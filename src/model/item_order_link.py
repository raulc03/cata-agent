from sqlmodel import SQLModel, Field


class ItemOrderLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int | None = Field(default=None, foreign_key="item.id")
    order_id: int | None = Field(default=None, foreign_key="order.id")
