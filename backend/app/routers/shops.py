from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Item, Shop
from app.schemas import (
    PaginatedShops,
    ShopBase,
    ShopChoice,
    ShopRead,
    ShopWarrantyItems,
    WarrantyItemRow,
)
from app.serializers import shop_read
from app.utils import (
    delete_shop_linked_items,
    paginate,
    shop_warranty_items,
)

router = APIRouter(prefix="/shops", tags=["shops"])


@router.get("/choices", response_model=list[ShopChoice])
def list_shop_choices(db: Session = Depends(get_db)):
    shops = db.scalars(select(Shop).order_by(func.lower(Shop.name))).all()
    return [ShopChoice(id=shop.id, name=shop.name) for shop in shops]


@router.get("", response_model=PaginatedShops)
def list_shops(page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    per_page = settings.records_per_page
    total = db.scalar(select(func.count()).select_from(Shop)) or 0
    meta = paginate(total, page, per_page)

    rows = db.execute(
        select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item)
        .group_by(Shop.id)
        .order_by(Shop.id)
        .offset((meta["page"] - 1) * per_page)
        .limit(per_page)
    ).all()

    items = [shop_read(shop, count) for shop, count in rows]
    return PaginatedShops(items=items, **meta)


@router.get("/{shop_id}", response_model=ShopRead)
def get_shop(shop_id: int, db: Session = Depends(get_db)):
    shop = db.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    items_count = db.scalar(select(func.count(Item.id)).where(Item.shop_id == shop.id)) or 0
    return shop_read(shop, items_count)


@router.get("/{shop_id}/warranty-items", response_model=ShopWarrantyItems)
def get_shop_warranty_items(shop_id: int, db: Session = Depends(get_db)):
    shop = db.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    under, out = shop_warranty_items(db, shop_id)
    return ShopWarrantyItems(
        under_warranty=[WarrantyItemRow(**row) for row in under],
        out_of_warranty=[WarrantyItemRow(**row) for row in out],
    )


@router.post("", response_model=ShopRead, status_code=201)
def create_shop(payload: ShopBase, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Shop name is required")

    existing = db.scalar(select(Shop.id).where(Shop.name == name))
    if existing:
        raise HTTPException(status_code=409, detail="Shop with this name already exists")

    shop = Shop(
        name=name,
        street=payload.street or "",
        city=payload.city or "",
        zip_code=payload.zip_code or "",
    )
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop_read(shop, 0)


@router.put("/{shop_id}", response_model=ShopRead)
def update_shop(shop_id: int, payload: ShopBase, db: Session = Depends(get_db)):
    shop = db.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Shop name is required")

    if name != shop.name:
        existing = db.scalar(select(Shop.id).where(Shop.name == name))
        if existing:
            raise HTTPException(status_code=409, detail="Shop with this name already exists")

    shop.name = name
    shop.street = payload.street or ""
    shop.city = payload.city or ""
    shop.zip_code = payload.zip_code or ""
    db.commit()

    items_count = db.scalar(select(func.count(Item.id)).where(Item.shop_id == shop.id)) or 0
    return shop_read(shop, items_count)


@router.delete("/{shop_id}", status_code=204)
def delete_shop(
    shop_id: int,
    linked_items: bool = Query(False),
    db: Session = Depends(get_db),
):
    shop = db.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    if linked_items:
        delete_shop_linked_items(db, shop_id)
    else:
        db.execute(update(Item).where(Item.shop_id == shop_id).values(shop_id=None))

    db.delete(shop)
    db.commit()
