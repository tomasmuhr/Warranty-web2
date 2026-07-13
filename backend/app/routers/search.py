from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Item, Shop, WarrantyDate
from app.routers.items import _item_read
from app.routers.shops import _shop_read
from app.schemas import SearchResults

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResults)
def search(query: str = Query("", min_length=1), db: Session = Depends(get_db)):
    pattern = f"%{query}%"

    item_rows = db.scalars(
        select(Item)
        .join(WarrantyDate, Item.id == WarrantyDate.item_id, isouter=True)
        .join(Shop, Item.shop_id == Shop.id, isouter=True)
        .options(joinedload(Item.dates), joinedload(Item.shop))
        .where(or_(Item.name.ilike(pattern), Item.comment.ilike(pattern)))
        .order_by(Item.name)
    ).unique().all()

    shop_rows = db.execute(
        select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .where(
            or_(
                Shop.name.ilike(pattern),
                Shop.street.ilike(pattern),
                Shop.city.ilike(pattern),
            )
        )
        .group_by(Shop.id)
        .order_by(Shop.name)
    ).all()

    return SearchResults(
        query=query,
        items=[_item_read(item) for item in item_rows],
        shops=[_shop_read(shop, count) for shop, count in shop_rows],
    )
