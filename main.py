import asyncio
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain.agents import ToolNode, create_agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()


# TODO: Crear base de datos
# TODO: Poblar base de datos
# TODO: Modificar tool para llamar a Base de datos
@tool
def search_items(
    item_name: str | None = None,
    item_size: str | None = None,
    item_code: str | None = None,
    item_price: float | None = None,
):
    """
    Search one item by specific attributes.
    """
    items = [
        {
            "item_name": "Classic Cotton T-Shirt",
            "item_size": "M",
            "item_code": "CCT-M001",
            "item_price": 19.99,
        },
        {
            "item_name": "Slim Fit Denim Jeans",
            "item_size": "L",
            "item_code": "SFJ-L032",
            "item_price": 59.99,
        },
        {
            "item_name": "Wool Blend Sweater",
            "item_size": "S",
            "item_code": "WBS-S045",
            "item_price": 79.99,
        },
        {
            "item_name": "Wool Blend Sweater",
            "item_size": "M",
            "item_code": "WBS-S045",
            "item_price": 79.99,
        },
        {
            "item_name": "Wool Blend Sweater",
            "item_size": "L",
            "item_code": "WBS-S045",
            "item_price": 79.99,
        },
        {
            "item_name": "Summer Floral Dress",
            "item_size": "M",
            "item_code": "SFD-M078",
            "item_price": 45.99,
        },
        {
            "item_name": "Leather Jacket",
            "item_size": "L",
            "item_code": "LJK-L021",
            "item_price": 129.99,
        },
        {
            "item_name": "Sports Running Shoes",
            "item_size": "S",
            "item_code": "SRS-009",
            "item_price": 89.99,
        },
        {
            "item_name": "Cotton Polo Shirt",
            "item_size": "L",
            "item_code": "CPS-L015",
            "item_price": 34.99,
        },
        {
            "item_name": "Winter Coat",
            "item_size": "XL",
            "item_code": "WCT-XL056",
            "item_price": 149.99,
        },
    ]

    query = {
        "item_name": item_name,
        "item_size": item_size,
        "item_code": item_code,
        "item_price": item_price,
    }

    for item in items:
        match = True
        for key, value in query.items():
            if value is not None:
                if isinstance(value, str):
                    if value.lower() not in item[key].lower():
                        match = False
                        break
                else:
                    if value != item[key]:
                        match = False
                        break
        if match:
            return item
    return {}


class Item(BaseModel):
    name: str = Field(description="Name of the clothe")
    size: str = Field(max_length=1, description="Size of the clothe")
    code: str = Field(description="Unique code of the clothe")
    price: float = Field(description="Price of the clothe")


class Order(BaseModel):
    items: list[Item] = Field(default=[], description="List of items")
    total_price: float = Field(description="Total price of the order")


tool_node = ToolNode(
    tools=[search_items],
    handle_tool_errors="Please check your input and try again.",
)


async def main():
    llm = init_chat_model("anthropic:claude-3-5-haiku-latest", api_key=os.getenv("API_KEY"))
    agent = create_agent(
        model=llm,
        tools=tool_node,
        prompt=SystemMessage(
            [
                ("You are an expert assistant in creating purchase orders."),
                (" Your task is to validate whether the items exist and return them in an order."),
            ]
        ),
        response_format=Order,
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Quiero el sweater de talla S y también las sport running shoes de talla S",
                }
            ]
        }
    )

    print(result["structured_response"])


if __name__ == "__main__":
    asyncio.run(main())
