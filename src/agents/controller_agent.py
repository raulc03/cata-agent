import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from agents.create_order_agent import agent as create_order_agent

_prompt = SystemMessage(
    "You are an expert sales assistant, and your responsibility will be to register user orders. "
    # "You should not add default values. If data is missing, the user must be notified. "
)

_model = init_chat_model(
    model="anthropic:claude-3-5-haiku-latest", api_key=os.getenv("API_KEY", ""), temperature=0.7
)

controller_agent = create_agent(model=_model, tools=[create_order_agent], prompt=_prompt)
