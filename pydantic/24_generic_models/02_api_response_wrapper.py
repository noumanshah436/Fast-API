"""
Generic API response envelope
=============================
One Response[T] schema for every endpoint -> uniform client parsing.
"""

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    # Envelope fields stay constant; only `data` varies per endpoint.
    status: str          # "ok" | "error"
    data: Optional[T] = None
    error: Optional[str] = None


class Order(BaseModel):
    id: int
    total: float


# Success case -- data is typed.
ok = Response[Order](status="ok", data=Order(id=7, total=49.99))
print(ok.model_dump())

# Error case -- data absent, error populated. Same shape on the wire.
err = Response[Order](status="error", error="ORDER_NOT_FOUND")
print(err.model_dump())

# Works with lists too.
bulk = Response[list[Order]](
    status="ok",
    data=[Order(id=1, total=10), Order(id=2, total=20)],
)
print(bulk.model_dump())
