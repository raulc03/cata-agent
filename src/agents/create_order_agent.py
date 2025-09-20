import os
from langchain.agents import ToolNode, create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from sqlmodel import Session, select
from decimal import Decimal

from model.item import Item, ItemAgent
from model.order import Order
from config.database import engine


_model = init_chat_model(
    model="anthropic:claude-3-5-haiku-latest", temperature=0.5, api_key=os.getenv("API_KEY", "")
)

_prompt = SystemMessage(
    "You are an expert assistant in validating the existence of items "
    "and summarizing them in a purchase order."
)

############################# tools ##################################


@tool
def create_items(
    item_name: str | None, item_size: str | None, item_color: str | None
) -> ItemAgent | str:
    """
    Use to validate that all require attributes from one item before create an order.
    """
    if item_name and item_size and item_color:
        return ItemAgent(name=item_name, size=item_size, color=item_color)
    else:
        return "Some required attributes are missing, please add them."


@tool
def get_correct_values() -> dict[str, list]:
    """
    Use to find out the values of the attributes
    that should replace those provided by the user before creating the order.
    """
    result = {"name": [], "size": [], "color": []}
    with Session(engine) as session:
        stmt = select(Item.name).distinct()
        result["name"] = list(session.exec(stmt).all())
        stmt = select(Item.size).distinct()
        result["size"] = list(session.exec(stmt).all())
        stmt = select(Item.color).distinct()
        result["color"] = list(session.exec(stmt).all())

    return result


@tool
def create_order(items: list[ItemAgent]) -> Order | str:
    """
    Use to search the items in database and create the order with them.
    If one item is not found, that item will be returned with a message.
    """
    bd_items: list[Item] = []
    with Session(engine) as session:
        for item in items:
            stmt = select(Item).where(Item.name.ilike(item.name))  # type:ignore
            stmt = stmt.where(Item.size.ilike(item.size))  # type:ignore
            stmt = stmt.where(Item.color.ilike(item.color))  # type:ignore

            result = session.exec(stmt).first()

            if result:
                bd_items.append(result)
            else:
                bd_items.clear()
                return f"This item was not found: {item}"

        if bd_items:
            total = sum([item.price for item in bd_items])
            if total == 0:
                total = Decimal(total)
            order = Order(items=bd_items, total_price=total)
            session.add(order)
            session.commit()
            session.refresh(order)
            return order
    return "There's no items"


############################# tools ##################################

_tool_node = ToolNode(tools=[create_items, get_correct_values, create_order])

sub_agent = create_agent(model=_model, tools=_tool_node, response_format=Order, prompt=_prompt)


@tool
def agent(items: list[ItemAgent]):
    """
    Use to create an order only with valid items.
    """
    result = sub_agent.invoke({"messages": HumanMessage(str(items))})
    return result["structured_response"]
