from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    name: str
    street: str = ""
    city: str = ""
    zip_code: str = ""


class ShopCreate(ShopBase):
    pass


class ShopUpdate(ShopBase):
    pass


class ShopRead(ShopBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items_count: int = 0


class ShopSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    street: str = ""
    city: str = ""
    zip_code: str = ""
    items_count: int = 0


class ShopChoice(BaseModel):
    id: int
    name: str


class ItemBase(BaseModel):
    name: str
    shop_id: Optional[int] = None
    receipt_nr: str = ""
    amount: Optional[float] = None
    price_per_piece: Optional[float] = None
    comment: str = ""
    purchase_date: date
    warranty_months: int = Field(ge=1)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    shop_id: Optional[int] = None
    shop_name: Optional[str] = None
    receipt_nr: str = ""
    amount: Optional[float] = None
    price_per_piece: Optional[float] = None
    comment: str = ""
    purchase_date: Optional[date] = None
    warranty_months: Optional[int] = None
    expiration_date: Optional[date] = None


class PaginatedShops(BaseModel):
    items: list[ShopRead]
    page: int
    per_page: int
    total: int
    pages: int


class PaginatedItems(BaseModel):
    items: list[ItemRead]
    page: int
    per_page: int
    total: int
    pages: int


class WarrantyItemRow(BaseModel):
    name: str
    purchase_date: date
    expiration_date: date


class ShopWarrantyItems(BaseModel):
    under_warranty: list[WarrantyItemRow]
    out_of_warranty: list[WarrantyItemRow]


class StatsRead(BaseModel):
    items_count: int
    shops_count: int


class SearchResults(BaseModel):
    query: str
    items: list[ItemRead]
    shops: list[ShopRead]


class DatabaseInfo(BaseModel):
    path: str


class PurgeRequest(BaseModel):
    option: Literal["warranties", "shops", "both"]


class MessageResponse(BaseModel):
    message: str
