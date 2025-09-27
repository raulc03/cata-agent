from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.item import Item
    from model.order import Order


class ItemOrderLink(SQLModel, table=True):
    item_id: int | None = Field(default=None, foreign_key="item.id", primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="order.id", primary_key=True)

    quantity: int = Field(default=1)

    item: "Item" = Relationship(back_populates="order_links")
    order: "Order" = Relationship(back_populates="item_links")
