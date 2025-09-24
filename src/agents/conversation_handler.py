import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage

from workflows.query_refiner import query_refiner_agent

_prompt = SystemMessage(
    "You are a conversational agent who will talk to the customer to manage a sales order. "
    "You will identify yourself as ‘Charito’ and don't say you're an assistant, just keep the conversation natural and friendly like the best sales agent. "
    "And you only speak in spanish.",
)

_model = init_chat_model(
    model="anthropic:claude-3-5-haiku-latest", api_key=os.getenv("API_KEY", ""), temperature=0.7
)

conversation_agent = create_agent(model=_model, tools=[query_refiner_agent], prompt=_prompt)
