from pathlib import Path

from agents.conversation_handler import conversation_agent
from config.database import create_db_and_table
from util.seed import insert_items


# TODO: Agregar el agente de confirmación con memoria de los mensajes con el cliente
def main():
    existsDB = Path("database.db").exists()
    create_db_and_table()
    if not existsDB:
        insert_items()

    response = conversation_agent.invoke(
        {
            "messages": ("user", input("Qué desea comprar: ")),
        }
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
