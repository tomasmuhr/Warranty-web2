from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Shop(Base):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    street: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    items: Mapped[list["Item"]] = relationship(back_populates="shop")


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    receipt_nr: Mapped[str] = mapped_column()
    amount: Mapped[float | None] = mapped_column()
    price_per_piece: Mapped[float | None] = mapped_column()
    comment: Mapped[str] = mapped_column()
    shop_id: Mapped[int | None] = mapped_column(ForeignKey("shop.id"), nullable=True)
    shop: Mapped["Shop | None"] = relationship(back_populates="items")
    dates: Mapped[list["WarrantyDate"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )


class WarrantyDate(Base):
    __tablename__ = "date"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=False)
    warranty_months: Mapped[int] = mapped_column(nullable=False)
    purchase_date: Mapped[date] = mapped_column(nullable=False)
    expiration_date: Mapped[date] = mapped_column(nullable=False)
    item: Mapped["Item"] = relationship(back_populates="dates")
