from pathlib import Path

from agents.conversation_handler import conversation_agent
from config.database import create_db_and_table
from util.seed import insert_items


def main():
    existsDB = Path("database.db").exists()
    create_db_and_table()
    if not existsDB:
        insert_items()

    first_loop = True

    while True:
        user_input = input("Cliente: ")
        if first_loop:
            response = conversation_agent.invoke(
                {
                    "messages": [("user", user_input)],  # type:ignore
                    "items": {},  # type:ignore
                },
                {"configurable": {"thread_id": "1"}},
            )
            first_loop = False
        else:
            response = conversation_agent.invoke(
                {
                    "messages": [("user", user_input)],  # type:ignore
                },
                {"configurable": {"thread_id": "1"}},
            )

        response["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()
