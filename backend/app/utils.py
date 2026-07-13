import math
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from dateutil.relativedelta import relativedelta
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Item, Shop, WarrantyDate


def paginate(total: int, page: int, per_page: int) -> dict:
    pages = max(1, math.ceil(total / per_page)) if total else 1
    page = min(max(page, 1), pages)
    return {"page": page, "per_page": per_page, "total": total, "pages": pages}


def expiration_date(purchase_date, warranty_months: int):
    return purchase_date + relativedelta(months=warranty_months)


def get_shop_choices(db: Session) -> list[str]:
    rows = db.scalars(select(Shop.name).order_by(func.lower(Shop.name))).all()
    return list(rows)


def allowed_backup_filename(filename: str) -> bool:
    return Path(filename).name == settings.db_name_backup


def is_warranty_app_database(path: Path) -> bool:
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        cur.close()
        conn.close()
        table_names = {table[0] for table in tables}
        return {"item", "date", "shop", "settings"}.issubset(table_names)
    except sqlite3.Error:
        return False


def purge_warranties(db: Session) -> None:
    item_ids = db.scalars(select(Item.id).where(Item.shop_id.is_(None))).all()
    if item_ids:
        db.execute(delete(WarrantyDate).where(WarrantyDate.item_id.in_(item_ids)))
        db.execute(delete(Item).where(Item.id.in_(item_ids)))
        db.commit()


def purge_shops(db: Session) -> None:
    rows = db.execute(
        select(Shop.id, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .group_by(Shop.id)
    ).all()
    empty_shop_ids = [row.id for row in rows if row.items_count == 0]
    if empty_shop_ids:
        db.execute(delete(Shop).where(Shop.id.in_(empty_shop_ids)))
        db.commit()


def export_database() -> Path:
    backup_path = settings.db_dir / settings.db_name_backup
    shutil.copyfile(settings.database_path, backup_path)
    return backup_path


def restore_database(upload_path: Path) -> None:
    db_path = settings.database_path
    backup_path = settings.db_dir / settings.db_name_backup
    shutil.copyfile(upload_path, backup_path)
    if not is_warranty_app_database(backup_path):
        backup_path.unlink(missing_ok=True)
        raise ValueError("The file is not a Warranty App database!")
    shutil.copyfile(backup_path, db_path)


def shop_warranty_items(db: Session, shop_id: int) -> tuple[list, list]:
    today = datetime.now().date()
    rows = db.execute(
        select(Item.name, WarrantyDate.purchase_date, WarrantyDate.expiration_date)
        .join(WarrantyDate, Item.id == WarrantyDate.item_id)
        .where(Item.shop_id == shop_id)
        .order_by(WarrantyDate.expiration_date.desc())
    ).all()

    under = [
        {"name": r.name, "purchase_date": r.purchase_date, "expiration_date": r.expiration_date}
        for r in rows
        if r.expiration_date >= today
    ]
    out = [
        {"name": r.name, "purchase_date": r.purchase_date, "expiration_date": r.expiration_date}
        for r in rows
        if r.expiration_date < today
    ]
    return under, out


def clear_shop_from_items(db: Session, shop_id: int) -> None:
    db.execute(update(Item).where(Item.shop_id == shop_id).values(shop_id=None))


def delete_shop_linked_items(db: Session, shop_id: int) -> None:
    item_ids = db.scalars(select(Item.id).where(Item.shop_id == shop_id)).all()
    if item_ids:
        db.execute(delete(WarrantyDate).where(WarrantyDate.item_id.in_(item_ids)))
        db.execute(delete(Item).where(Item.id.in_(item_ids)))
