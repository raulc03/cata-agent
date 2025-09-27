from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel

from model.item_order_link import ItemOrderLink
from model.item import ItemAgent


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    total_price: Decimal = Field(decimal_places=2)

    item_links: list[ItemOrderLink] = Relationship(back_populates="order")


class OrderAgent(BaseModel):
    items: list[ItemAgent] = Field(description="List of existing items.")
    total_price: Decimal = Field(
        decimal_places=2,
        description="Total order price consisting of the sum of the prices of all items.",
    )
