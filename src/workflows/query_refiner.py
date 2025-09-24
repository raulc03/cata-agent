import os
from typing import Any
import chromadb
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr


from dotenv import load_dotenv

load_dotenv()


@tool
def search_vector_store(raw_input: str, page_of_catalog: int) -> list[Any]:
    """
    Tool for semantically searching for items similar to the entry provided by the customer.
    """
    # set embedding function
    embedding_function = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=SecretStr(os.getenv("OPENAI_API_KEY", ""))
    )
    # set up Chroma connection
    client = chromadb.PersistentClient(path="chroma.db")
    collection = client.get_collection("text_collection")

    embedding_query = embedding_function.embed_query(raw_input)

    res = collection.query(
        query_embeddings=[embedding_query], n_results=10, where={"page": page_of_catalog}
    )

    if res["documents"]:
        return res["documents"]

    return []


@tool
def query_refiner_agent(item_raw_query: str) -> str:
    """
    Agent responsible for processing a single item within the user's query at a time
    with the aim of refining the attributes with real data from the database.
    """
    llm = init_chat_model(
        model="anthropic:claude-3-5-haiku-latest", api_key=os.getenv("API_KEY", "")
    )
    query_refiner = create_agent(
        model=llm,
        tools=[search_vector_store],
    )
    result = query_refiner.invoke(
        {"messages": ("user", f"Item from the customer: {item_raw_query}")}
    )

    return result["messages"][-1].content
