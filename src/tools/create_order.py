from decimal import Decimal
from typing import Annotated
from langchain.agents.tool_node import InjectedState
from langchain.tools import tool
from sqlmodel import Session, select

from model.item import Item
from model.item_order_link import ItemOrderLink
from model.order import Order
from config.database import engine
from tools.item_validator import CustomState


@tool(
    description="Adds the prices of multiple items and returns the total. "
    "Accepts any number of numeric values (prices) as arguments and returns the total sum as a number. "
    "Useful for calculating the total cost of a purchase, budget, or billing."
)
def sum_prices(*args) -> Decimal:
    return Decimal(sum(args))


@tool(
    description="Use this tool to create an order with the items "
    "and complete information ONLY when the customer has already confirmed the items they will purchase."
)
def create_order(state: Annotated[CustomState, InjectedState], total_price: Decimal) -> Order:
    order = Order(total_price=total_price)

    with Session(engine) as session:
        session.add(order)
        for id, quantity in state["items"].items():
            item = session.exec(select(Item).where(Item.id == id)).first()
            if item:
                new_item_order = ItemOrderLink(item=item, order=order, quantity=quantity)
                session.add(new_item_order)
        session.commit()
        session.refresh(order)

    return order
