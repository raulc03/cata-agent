import operator
import os
from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langgraph.types import Send
from pydantic import BaseModel
from sqlmodel import Session, select

from model.item import Item
from model.order import Order
from config.database import engine

from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    user_input: str
    user_items: list[Item]
    correct_items: Annotated[list, operator.add]
    final_items: list[Item]
    incorrect_items: list[Item]
    order: Order
    reply: str


class WorkState(TypedDict):
    input_item: Item
    correct_items: Annotated[list, operator.add]


class Items(BaseModel):
    items: list[Item]


# Nodes
def generate_items(state: State):
    """
    Create items based on the user input
    """
    llm = init_chat_model(
        model="anthropic:claude-3-5-haiku-latest", temperature=0.5, api_key=os.getenv("API_KEY", "")
    )
    system = SystemMessage(
        "You are an expert at analyzing and structuring texts. "
        "Your task is to create items based on the user's text request. "
        "If the user does not enter an attribute, that attribute will have the value ‘na’ if it is a string or 0. "
    )

    messages = [system, HumanMessage(state["user_input"])]

    llm_with_structured_output = llm.with_structured_output(Items)

    items = llm_with_structured_output.invoke(messages)

    if isinstance(items, Items):
        return {"user_items": items.items}
    else:
        return {"user_items": []}


def correct_items(state: WorkState):
    """
    Validate if items exists in the database.
    """
    llm = init_chat_model(
        model="anthropic:claude-3-5-haiku-latest",
        temperature=0.8,
        api_key=os.getenv("API_KEY", ""),
    )
    unique_names = ["B - Casaca"]
    unique_colors = ["Azul Marino", "Rojo Vino"]

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a specialist in matching items entered by customers with items in the database. "
                "Your task is to correct the names and colors of items that are most similar through semantic search. "
                "If the item entered by the user does not match any item in the database, either by name or color, change the name of the item to 'Item not found'. "
                "Here are the lists of valid names: {unique_names} "
                "And here is the list of valid colors: {unique_colors}",
            ),
            ("user", "Item to correct: {item}"),
        ]
    )

    llm_with_structured_output = llm.with_structured_output(Item)

    chain = prompt | llm_with_structured_output

    new_item = chain.invoke(
        {"unique_names": unique_names, "unique_colors": unique_colors, "item": state["input_item"]}
    )

    if isinstance(new_item, Item):
        if new_item.name == "Item not found":
            new_item.name = state["input_item"].name
            new_item.size = "B"

        if new_item.size != "B":
            with Session(engine) as session:
                item_bd = session.exec(
                    select(Item)
                    .where(Item.name == new_item.name)
                    .where(Item.size == new_item.size)
                    .where(Item.color == new_item.color)
                ).first()
                if item_bd:
                    return {"correct_items": [item_bd]}
    return {"correct_items": [new_item]}


def synthesizer(state: State):
    """Synthesize all the items"""

    return {
        "final_items": [item for item in state["correct_items"] if item.size != "B"],
        "incorrect_items": [item for item in state["correct_items"] if item.size == "B"],
    }


def assign_workers(state: State):
    """Asign a worker for each item in the list"""
    return [Send("correct_items", {"input_item": i}) for i in state["user_items"]]


def call_workflow():
    workflow = StateGraph(State)

    # Nodes
    workflow.add_node("generate_items", generate_items)
    workflow.add_node("correct_items", correct_items)
    workflow.add_node("synthesizer", synthesizer)

    # Edges
    workflow.add_edge(START, "generate_items")
    workflow.add_conditional_edges("generate_items", assign_workers, ["correct_items"])
    workflow.add_edge("correct_items", "synthesizer")
    workflow.add_edge("synthesizer", END)

    chain = workflow.compile()

    inp = input("Cuál es su pedido: ")
    state = chain.invoke({"user_input": inp})

    print(f"Correctos: {state['final_items']}")
    print(f"Incorrectos: {state['incorrect_items']}")
