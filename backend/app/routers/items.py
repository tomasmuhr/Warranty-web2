from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, select, asc, desc
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.database import get_db
from app.models import Item, Shop, WarrantyDate
from app.schemas import ItemBase, ItemRead, PaginatedItems
from app.serializers import item_read
from app.utils import expiration_date, paginate

router = APIRouter(prefix="/items", tags=["items"])

EXPIRING_SOON_DAYS = 30

SORTABLE_COLUMNS = {
    "id": Item.id,
    "name": Item.name,
    "shop_name": func.lower(Shop.name),
    "receipt_nr": Item.receipt_nr,
    "amount": Item.amount,
    "price_per_piece": Item.price_per_piece,
    "comment": Item.comment,
    "purchase_date": WarrantyDate.purchase_date,
    "warranty_months": WarrantyDate.warranty_months,
    "expiration_date": WarrantyDate.expiration_date,
}


def _warranty_filter_conditions(status: str | None) -> list:
    if not status:
        return []

    today = date.today()
    if status == "active":
        return [WarrantyDate.expiration_date >= today]
    if status == "expired":
        return [WarrantyDate.expiration_date < today]
    if status == "expiring":
        return [
            WarrantyDate.expiration_date >= today,
            WarrantyDate.expiration_date <= today + timedelta(days=EXPIRING_SOON_DAYS),
        ]
    return []


def _shop_filter_conditions(shop_id: int | None, no_shop: bool) -> list:
    if no_shop:
        return [Item.shop_id.is_(None)]
    if shop_id is not None:
        return [Item.shop_id == shop_id]
    return []


def _needs_warranty_join(sort_by: str, status: str | None) -> bool:
    return sort_by in {"purchase_date", "warranty_months", "expiration_date"} or bool(status)


@router.get("", response_model=PaginatedItems)
def list_items(
    page: int = Query(1, ge=1),
    sort_by: str = Query("id"),
    sort_dir: str = Query("asc", pattern="^(asc|desc)$"),
    status: str | None = Query(None, pattern="^(active|expiring|expired)$"),
    shop_id: int | None = Query(None, ge=1),
    no_shop: bool = Query(False),
    db: Session = Depends(get_db),
):
    per_page = settings.records_per_page
    filter_conditions = [
        *_shop_filter_conditions(shop_id, no_shop),
        *_warranty_filter_conditions(status),
    ]
    needs_warranty = _needs_warranty_join(sort_by, status)

    count_stmt = select(func.count()).select_from(Item)
    if needs_warranty:
        count_stmt = count_stmt.join(WarrantyDate, Item.id == WarrantyDate.item_id)
    if filter_conditions:
        count_stmt = count_stmt.where(*filter_conditions)

    total = db.scalar(count_stmt) or 0
    meta = paginate(total, page, per_page)

    column = SORTABLE_COLUMNS.get(sort_by, Item.id)
    order = asc(column) if sort_dir == "asc" else desc(column)
    query = select(Item).options(joinedload(Item.dates), joinedload(Item.shop))
    if sort_by == "shop_name":
        query = query.outerjoin(Shop)
    if needs_warranty:
        if status:
            query = query.join(WarrantyDate, Item.id == WarrantyDate.item_id)
        else:
            query = query.outerjoin(WarrantyDate)
    if filter_conditions:
        query = query.where(*filter_conditions)

    items = (
        db.scalars(
            query.order_by(order, Item.id)  # stable tie-breaker
            .offset((meta["page"] - 1) * per_page)
            .limit(per_page)
        )
        .unique()
        .all()
    )
    return PaginatedItems(items=[item_read(item) for item in items], **meta)


@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemBase, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Item name is required")

    if payload.shop_id is not None and not db.get(Shop, payload.shop_id):
        raise HTTPException(status_code=400, detail="Selected shop does not exist")

    item = Item(
        name=name,
        shop_id=payload.shop_id,
        receipt_nr=payload.receipt_nr or "",
        amount=payload.amount,
        price_per_piece=payload.price_per_piece,
        comment=payload.comment or "",
    )
    warranty = WarrantyDate(
        item=item,
        purchase_date=payload.purchase_date,
        warranty_months=payload.warranty_months,
        expiration_date=expiration_date(payload.purchase_date, payload.warranty_months),
    )
    item.dates.append(warranty)
    db.add(item)
    db.commit()
    db.refresh(item)
    item = (
        db.scalars(
            select(Item)
            .options(joinedload(Item.dates), joinedload(Item.shop))
            .where(Item.id == item.id)
        )
        .unique()
        .one()
    )
    return item_read(item)


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemBase, db: Session = Depends(get_db)):
    item = (
        db.scalars(
            select(Item)
            .options(joinedload(Item.dates), joinedload(Item.shop))
            .where(Item.id == item_id)
        )
        .unique()
        .one_or_none()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Item name is required")

    if payload.shop_id is not None and not db.get(Shop, payload.shop_id):
        raise HTTPException(status_code=400, detail="Selected shop does not exist")

    item.name = name
    item.shop_id = payload.shop_id
    item.receipt_nr = payload.receipt_nr or ""
    item.amount = payload.amount
    item.price_per_piece = payload.price_per_piece
    item.comment = payload.comment or ""

    if not item.dates:
        item.dates.append(
            WarrantyDate(
                item_id=item.id,
                warranty_months=1,
                purchase_date=payload.purchase_date,
                expiration_date=payload.purchase_date,
            )
        )

    warranty = item.dates[0]
    warranty.purchase_date = payload.purchase_date
    warranty.warranty_months = payload.warranty_months
    warranty.expiration_date = expiration_date(
        payload.purchase_date, payload.warranty_months
    )

    db.commit()
    db.refresh(item)
    return item_read(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.execute(delete(WarrantyDate).where(WarrantyDate.item_id == item_id))
    db.delete(item)
    db.commit()
