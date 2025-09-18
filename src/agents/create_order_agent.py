import os
from langchain.agents import ToolNode, create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from sqlmodel import Session, select

from model.item import Item, ItemAgent
from model.order import OrderAgent
from config.database import engine

from dotenv import load_dotenv

load_dotenv()

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
    Use to validate that all require attributes from one item.
    """
    if item_name and item_size and item_color:
        return ItemAgent(name=item_name, size=item_size, color=item_color)
    else:
        return "Some required attributes are missing, please add them."


@tool
def find_items(items: list[ItemAgent]):
    """
    Use to find the items in the database in order to know if exists.
    If one item doesn't exists, the order
    """
    bd_items = []
    with Session(engine) as session:
        for item in items:
            # TODO: Agregar la búsqueda mediante 'ilike'
            stmt = select(Item).where(Item.name == item.name)
            stmt = stmt.where(Item.size == item.size)
            stmt = stmt.where(Item.color == item.color)

            result = session.exec(stmt).first()

            if result:
                bd_items.append(result)
            else:
                bd_items.clear()
                break

    # TODO: En caso un item falle, retornarlo como fallido para que se le haga saber al usuario
    if bd_items:
        return bd_items
    else:
        return "This item was not found"


############################# tools ##################################

_tool_node = ToolNode(tools=[create_items])

sub_agent = create_agent(model=_model, tools=_tool_node, response_format=OrderAgent, prompt=_prompt)


@tool
def agent(items: list[ItemAgent]):
    """
    Use to create an order only with valid items.
    """
    result = sub_agent.invoke({"messages": HumanMessage(str(items))})
    return result["structured_response"]
