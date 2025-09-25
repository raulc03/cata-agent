import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

from prompts.conversation_handler import SYSTEM_PROMPT_V0
from tools.item_validator import validate_item
from tools.query_refiner import refine_requested_item

from dotenv import load_dotenv

load_dotenv()

_prompt = SystemMessage(SYSTEM_PROMPT_V0)

_model = init_chat_model(
    model="anthropic:claude-3-7-sonnet-latest", api_key=os.getenv("API_KEY", ""), temperature=0.5
)

conversation_agent = create_agent(
    model=_model,
    tools=[refine_requested_item, validate_item],
    prompt=_prompt,
    checkpointer=InMemorySaver(),
)
