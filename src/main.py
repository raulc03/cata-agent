from pathlib import Path

from langchain_core.messages import HumanMessage
from agents.controller_agent import controller_agent
from config.database import create_db_and_table
from util.seed import insert_items


def main():
    existsDB = Path("database.db").exists()
    create_db_and_table()
    if not existsDB:
        insert_items()

    response = controller_agent.invoke(
        {
            "messages": HumanMessage(input("Qué desea comprar: ")),
        }
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
