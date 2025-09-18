from sqlmodel import SQLModel, Field


class ItemOrderLink(SQLModel, table=True):
    item_id: int | None = Field(default=None, foreign_key="item.id", primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="order.id", primary_key=True)
