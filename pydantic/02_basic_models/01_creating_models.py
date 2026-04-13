"""
Creating Models
===============
Subclass BaseModel, declare typed fields — that's the whole API.

Supported types (common ones)
-----------------------------
scalars     →  str, int, float, bool, bytes, Decimal
datetime    →  datetime, date, time, timedelta   (ISO strings accepted)
ids         →  UUID, Enum (by value)
collections →  list[X], dict[K, V], set[X], tuple[X, Y]
nullable    →  X | None                          (still required unless `= None`)
nested      →  any other BaseModel

Three ways to instantiate — same pipeline, different ergonomics
---------------------------------------------------------------
Model(a=1, b=2)              kwargs           — hand-written call sites
Model(**data)                dict-spread      — known-shape dicts, DB rows
Model.model_validate(data)   explicit verb    — dynamic input, from_attributes, nested

Lax coercions that "just work"
------------------------------
"49.99"   → float          "2025-01-01T10:00" → datetime
1 / 0     → True / False   "f47ac10b-..."     → UUID
"""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class Product(BaseModel):
    id: UUID
    name: str
    price: float
    in_stock: bool
    # Mutable defaults are safe in Pydantic — each instance gets its own copy
    # (unlike plain Python classes, where `[]` would be shared).
    tags: list[str] = []
    created_at: datetime


# Mixed-type input shows lax coercion in action:
# str→float, int→bool, ISO-string→datetime all happen automatically.
p = Product(
    id=uuid4(),
    name="Keyboard",
    price="49.99",                # str -> float coercion
    in_stock=1,                   # 1/0 -> True/False
    created_at="2025-01-01T10:00:00",
)
print(p.model_dump())


# Dict-spread — the natural shape of API payloads and DB rows.
row = {"id": uuid4(), "name": "Mouse", "price": 19.99,
       "in_stock": True, "tags": ["wireless"], "created_at": datetime.now()}
print(Product(**row))
