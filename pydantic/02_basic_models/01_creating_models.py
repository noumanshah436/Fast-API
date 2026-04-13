"""
Creating Models
===============
Subclass BaseModel, declare typed fields -- that is the whole API surface.
"""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class Product(BaseModel):
    # Pydantic validates and coerces each field against the type hint.
    id: UUID
    name: str
    price: float
    in_stock: bool
    tags: list[str] = []          # mutable defaults are safe in Pydantic
    created_at: datetime          # ISO strings like "2025-01-01T10:00" also work


# 1. Keyword arguments -- natural when you have individual values.
p1 = Product(
    id=uuid4(),
    name="Keyboard",
    price="49.99",                # str -> float coercion
    in_stock=1,                   # 1/0 -> True/False
    created_at="2025-01-01T10:00:00",
)
print(p1.name, p1.price, p1.in_stock)


# 2. Dict unpacking -- natural when the data comes from an API or DB row.
row = {
    "id": uuid4(),
    "name": "Mouse",
    "price": 19.99,
    "in_stock": True,
    "tags": ["peripherals", "wireless"],
    "created_at": datetime.now(),
}
p2 = Product(**row)
print(p2.tags, p2.created_at)
