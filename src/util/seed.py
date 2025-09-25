from decimal import Decimal
from sqlmodel import Session

from config.database import engine
from model.item import Item

items = [
    Item(
        name="D - Chaleco",
        code=678807,
        color="Beige",
        price=Decimal("49.90"),
        size="XS",
        catalog="625635",
    ),
    Item(
        name="D - Chaleco",
        code=678808,
        color="Beige",
        price=Decimal("49.90"),
        size="S",
        catalog="625635",
    ),
    Item(
        name="D - Chaleco",
        code=678809,
        color="Beige",
        price=Decimal("49.90"),
        size="M",
        catalog="625635",
    ),
    Item(
        name="D - Chaleco",
        code=678810,
        color="Beige",
        price=Decimal("49.90"),
        size="L",
        catalog="625635",
    ),
    Item(
        name="D - Chaleco",
        code=678811,
        color="Beige",
        price=Decimal("49.90"),
        size="XL",
        catalog="625635",
    ),
    Item(
        name="D - Chaleco",
        code=678812,
        color="Beige",
        price=Decimal("49.90"),
        size="XXL",
        catalog="625635",
    ),
    # ---- PANTALÓN ----
    Item(
        name="E - Pantalon",
        code=678904,
        color="Beige",
        price=Decimal("79.90"),
        size="26",
        catalog="625636",
    ),
    Item(
        name="E - Pantalon",
        code=678905,
        color="Beige",
        price=Decimal("79.90"),
        size="28",
        catalog="625636",
    ),
    Item(
        name="E - Pantalon",
        code=678906,
        color="Beige",
        price=Decimal("79.90"),
        size="30",
        catalog="625636",
    ),
    Item(
        name="E - Pantalon",
        code=678907,
        color="Beige",
        price=Decimal("79.90"),
        size="32",
        catalog="625636",
    ),
    Item(
        name="E - Pantalon",
        code=678908,
        color="Beige",
        price=Decimal("79.90"),
        size="34",
        catalog="625636",
    ),
    Item(
        name="E - Pantalon",
        code=678909,
        color="Beige",
        price=Decimal("79.90"),
        size="36",
        catalog="625636",
    ),
]


def insert_items():
    with Session(engine) as session:
        for it in items:
            session.add(it)
        session.commit()
