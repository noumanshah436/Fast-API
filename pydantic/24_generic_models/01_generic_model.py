"""
Generic pagination wrapper
==========================
v2: inherit from BaseModel AND Generic[T]. v1's GenericModel is gone.
"""

from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    # Items keep their concrete type -- Page[User] validates each entry as User.
    items: list[T]
    total: int
    page: int = 1
    size: int = 20


class User(BaseModel):
    id: int
    email: str


# Parameterize at use-site. Pydantic builds a specialized validator.
users_page = Page[User](
    items=[{"id": 1, "email": "a@x.io"}, {"id": 2, "email": "b@x.io"}],
    total=2,
)
print(users_page.model_dump())

# Same wrapper, different payload type -- no code duplication.
str_page = Page[str](items=["alpha", "beta"], total=2)
print(str_page)

# FastAPI usage:
#   @app.get("/users", response_model=Page[User])
#   def list_users(...): ...
