"""
Generic pagination wrapper
==========================
One container schema, many payload types — typed at use-site, validated per item.

v1 vs v2
--------
v1                                    v2
-------------------------------------------------------------
from pydantic.generics import        from typing import Generic, TypeVar
    GenericModel                     class X(BaseModel, Generic[T]): ...
class X(GenericModel, Generic[T])    GenericModel base class is GONE

How it works:
- Inherit from BOTH `BaseModel` and `Generic[T]`
- `Page[User]` builds a specialized validator; items are coerced to User
- Each specialization is cached -- cheap to reuse

Gotchas:
- Forgetting `Generic[T]` -> T stays Any and no per-item validation
- Bare `Page` (unparameterized) accepts anything for `items`
- TypeVars must be module-level -- don't define inside the class
"""

from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    # `list[T]` becomes `list[User]` when Page[User] is used -- real validation.
    items: list[T]
    total: int
    page: int = 1
    size: int = 20


class User(BaseModel):
    id: int
    email: str


# Parameterize at the call-site. Dict inputs are validated against User.
users_page = Page[User](
    items=[{"id": 1, "email": "a@x.io"}, {"id": 2, "email": "b@x.io"}],
    total=2,
)
print(users_page.model_dump())

# Same wrapper, primitive payload -- no duplication across endpoints.
str_page = Page[str](items=["alpha", "beta"], total=2)
print(str_page)

# FastAPI usage:
#   @app.get("/users", response_model=Page[User])
#   def list_users(...): ...
