from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING

# from model.item_order_link import ItemOrderLink

if TYPE_CHECKING:
    from model.order import Order


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: int
    color: str
    price: Decimal = Field(decimal_places=2)
    size: str = Field(max_length=2)
    catalog: str
    created_at: datetime = Field(default_factory=datetime.now)

    # orders: list["Order"] = Relationship(back_populates="items", link_model=ItemOrderLink)


class ItemAgent(BaseModel):
    name: str = Field(description="Name of the item, the user must assign it.")
    size: str = Field(
        max_length=2,
        description="Size of the item, there is no default value, so the user must add it.",
    )
    code: int | None = Field(
        default=None, description="Unique code of the clothe, the user can skip it."
    )
    color: str = Field(description="Color of the item, the user must assign it.")
