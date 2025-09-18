from decimal import Decimal
from sqlmodel import Session

from config.database import engine
from model.item import Item


items_dict = [
    {
        "name": "B - Casaca",
        "code": 1001,
        "color": "Azul Marino",
        "price": Decimal("29.99"),
        "size": "M",
        "catalog": "Ropa Casual",
    },
    {
        "name": "B - Casaca",
        "code": 1002,
        "color": "Azul Marino",
        "price": Decimal("29.99"),
        "size": "S",
        "catalog": "Ropa Casual",
    },
    {
        "name": "B - Casaca",
        "code": 1003,
        "color": "Azul Marino",
        "price": Decimal("29.99"),
        "size": "L",
        "catalog": "Ropa Casual",
    },
    {
        "name": "B - Casaca",
        "code": 1004,
        "color": "Rojo Vino",
        "price": Decimal("29.99"),
        "size": "L",
        "catalog": "Ropa Casual",
    },
]


def insert_items():
    with Session(engine) as session:
        for it in items_dict:
            item = Item(**it)
            session.add(item)
        session.commit()
