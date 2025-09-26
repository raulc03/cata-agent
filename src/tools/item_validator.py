from operator import add
from typing import Annotated
from langchain.agents import AgentState
from langchain_core import messages
from langgraph.types import Command
from sqlmodel import Session, select
from langchain.tools import InjectedToolCallId, tool

from config.database import engine
from model.item import Item
from util import normalize_name


class CustomState(AgentState):
    items: Annotated[list[Item], add]


@tool
def validate_item(
    name: str,
    color: str,
    size: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
    code: str | None = None,
) -> Command:
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
            return Command(
                update={
                    "items": [item],
                    "messages": [
                        messages.ToolMessage(str(item.model_dump()), tool_call_id=tool_call_id)
                    ],
                }
            )
        else:
            return Command(
                update={
                    "messages": [messages.ToolMessage("Item not exists", tool_call_id=tool_call_id)]
                }
            )
