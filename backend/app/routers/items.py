from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.database import get_db
from app.models import Item, Shop, WarrantyDate
from app.schemas import ItemCreate, ItemRead, ItemUpdate, PaginatedItems
from app.utils import expiration_date, paginate

router = APIRouter(prefix="/items", tags=["items"])


def _item_read(item: Item) -> ItemRead:
    warranty = item.dates[0] if item.dates else None
    shop_name = item.shop.name if item.shop else None
    return ItemRead(
        id=item.id,
        name=item.name,
        shop_id=item.shop_id,
        shop_name=shop_name,
        receipt_nr=item.receipt_nr or "",
        amount=item.amount,
        price_per_piece=item.price_per_piece,
        comment=item.comment or "",
        purchase_date=warranty.purchase_date if warranty else None,
        warranty_months=warranty.warranty_months if warranty else None,
        expiration_date=warranty.expiration_date if warranty else None,
    )


@router.get("", response_model=PaginatedItems)
def list_items(page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    per_page = settings.records_per_page
    total = db.scalar(select(func.count()).select_from(Item)) or 0
    meta = paginate(total, page, per_page)

    items = db.scalars(
        select(Item)
        .options(joinedload(Item.dates), joinedload(Item.shop))
        .order_by(Item.id)
        .offset((meta["page"] - 1) * per_page)
        .limit(per_page)
    ).unique().all()

    return PaginatedItems(items=[_item_read(item) for item in items], **meta)


@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
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
    item = db.scalars(
        select(Item)
        .options(joinedload(Item.dates), joinedload(Item.shop))
        .where(Item.id == item.id)
    ).unique().one()
    return _item_read(item)


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.scalars(
        select(Item)
        .options(joinedload(Item.dates), joinedload(Item.shop))
        .where(Item.id == item_id)
    ).unique().one_or_none()
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
        item.dates.append(WarrantyDate(item_id=item.id, warranty_months=1, purchase_date=payload.purchase_date, expiration_date=payload.purchase_date))

    warranty = item.dates[0]
    warranty.purchase_date = payload.purchase_date
    warranty.warranty_months = payload.warranty_months
    warranty.expiration_date = expiration_date(payload.purchase_date, payload.warranty_months)

    db.commit()
    db.refresh(item)
    return _item_read(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.execute(delete(WarrantyDate).where(WarrantyDate.item_id == item_id))
    db.delete(item)
    db.commit()
