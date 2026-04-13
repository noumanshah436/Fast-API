"""
Generic API response envelope
=============================
One `Response[T]` shape for every endpoint -> clients parse once, reuse forever.

Envelope shape
--------------
Field     Type              Purpose
-------------------------------------------------------------
status    "ok" | "error"    machine-readable outcome
data      Optional[T]       payload on success, None on failure
error     Optional[str]     human/code string on failure

Why this pattern:
- Uniform wire shape -> single parser in the client SDK
- `T` varies per endpoint, outer structure stays identical
- Pairs with `Page[T]` for paginated list endpoints: `Response[Page[Order]]`

Gotchas:
- v2 does NOT auto-default `Optional[X]` to None -- write `= None`
- Don't leak exception messages in `error` -- use stable error codes
- Nesting generics (Response[Page[T]]) works but keep depth sane
"""

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    # Envelope is invariant; only `data` changes per endpoint.
    status: str          # "ok" | "error"
    data: Optional[T] = None
    error: Optional[str] = None


class Order(BaseModel):
    id: int
    total: float


# Success: data is typed as Order, fully validated.
ok = Response[Order](status="ok", data=Order(id=7, total=49.99))
print(ok.model_dump())

# Failure: same wire shape, data omitted. Clients branch on `status`.
err = Response[Order](status="error", error="ORDER_NOT_FOUND")
print(err.model_dump())

# Generics compose -- list payload works the same way.
bulk = Response[list[Order]](
    status="ok",
    data=[Order(id=1, total=10), Order(id=2, total=20)],
)
print(bulk.model_dump())
