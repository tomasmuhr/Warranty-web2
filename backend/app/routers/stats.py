from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item, Shop
from app.schemas import StatsRead

router = APIRouter(tags=["stats"])


@router.get("/stats", response_model=StatsRead)
def get_stats(db: Session = Depends(get_db)):
    items_count = db.scalar(select(func.count(Item.id))) or 0
    shops_count = db.scalar(select(func.count(Shop.id))) or 0
    return StatsRead(items_count=items_count, shops_count=shops_count)
