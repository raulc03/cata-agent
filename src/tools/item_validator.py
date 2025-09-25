from sqlmodel import Session, select
from langchain.tools import tool

from config.database import engine
from model.item import Item
from util import normalize_name


@tool
def validate_item(name: str, color: str, size: str, code: str | None = None) -> Item | None:
    """
    Use to validate the existence of only one item in the database by its
    name, color, size or code retrieved by the query refiner.
    """
    std_name = normalize_name(name)
    stmt = None
    if code:
        stmt = select(Item).where(Item.code == code)
    else:
        stmt = (
            select(Item)
            .where(Item.name.ilike(f"%{std_name}%"))  # type:ignore
            .where(Item.color.ilike(f"%{color}%"))  # type:ignore
            .where(Item.size == size)
        )
    with Session(engine) as session:
        item = session.exec(stmt).first()
        if item:
            return item
        else:
            return None
