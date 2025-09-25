import os
import chromadb
from typing import Any
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import SecretStr

from prompts.query_refiner import SYSTEM_PROMPT_V0


@tool(
    description="This tool is used to refine the values of an item in the customer's order according to the specified page. Only one purchase item will be refined at a time"
)
def refine_requested_item(requested_item: str, page_of_catalog: int) -> Any:
    """
    Refines a requested item by validating and adjusting its attributes
    according to the given catalog page.

    Args:
        requested_item (str): Raw description or identifier of the requested item.
        page_of_catalog (int): Page number of the catalog to use as reference.

    Returns:
        str: refined representation of the item.
        The exact structure of each element depends on the catalog’s data model.
    """
    embedding_function = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=SecretStr(os.getenv("OPENAI_API_KEY", ""))
    )
    client = chromadb.PersistentClient(path="chroma.db")
    collection = client.get_collection("text_collection")

    embedding_query = embedding_function.embed_query(requested_item)

    res = collection.query(
        query_embeddings=[embedding_query], n_results=5, where={"page": page_of_catalog}
    )

    llm = init_chat_model(
        model="anthropic:claude-3-5-haiku-latest",
        api_key=os.getenv("API_KEY", ""),
        temperature=0.5,
    )

    response = llm.invoke(
        [
            SystemMessage(SYSTEM_PROMPT_V0),
            HumanMessage(f"Requested item: {requested_item}\nSearch result: {res['documents']}"),
        ]
    )

    return response.content
