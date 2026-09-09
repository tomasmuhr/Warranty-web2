from app.models import Item, Shop
from app.schemas import ItemRead, ShopRead


def item_read(item: Item) -> ItemRead:
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


def shop_read(shop: Shop, items_count: int) -> ShopRead:
    return ShopRead(
        id=shop.id,
        name=shop.name,
        street=shop.street or "",
        city=shop.city or "",
        zip_code=shop.zip_code or "",
        items_count=items_count,
    )
