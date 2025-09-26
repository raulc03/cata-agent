from decimal import Decimal
from typing import Annotated
from langchain.agents.tool_node import InjectedState
from langchain.tools import tool
from sqlmodel import Session

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
        for item in state["items"]:
            merged_item = session.merge(item)
            merged_item.orders.append(order)
            session.add(merged_item)
        session.commit()
        session.refresh(order)

    return order
