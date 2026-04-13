"""
from_attributes (formerly "ORM mode")
=====================================
Build a Pydantic model from any object -- read fields via getattr, not dict keys.

Input shape          Works by default?   Works with from_attributes=True?
-----------------------------------------------------------------------------
dict / JSON          yes                 yes
SQLAlchemy row       NO (expects dict)   yes
dataclass instance   NO                  yes
arbitrary object     NO                  yes  (anything with matching attrs)

Why v2 renamed it:
  v1 `orm_mode=True`  →  v2 `from_attributes=True`
  Same feature, clearer name -- it isn't really ORM-specific.

Typical FastAPI flow:
  DB query → SQLAlchemy row → UserRead.model_validate(row) → JSON response.
"""

from pydantic import BaseModel, ConfigDict


# Stand-in for a SQLAlchemy mapped class / any attribute-bearing object.
class UserORM:
    def __init__(self, id: int, email: str, is_admin: bool):
        self.id = id
        self.email = email
        self.is_admin = is_admin


class UserRead(BaseModel):
    # Without this flag, model_validate(orm_row) would raise -- it'd try to
    # treat the row as a mapping and fail the subscript check.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_admin: bool


row = UserORM(id=1, email="ada@example.com", is_admin=False)

# Pydantic walks the object's attributes and validates each field.
user = UserRead.model_validate(row)
print(user.model_dump())
# {'id': 1, 'email': 'ada@example.com', 'is_admin': False}

# Pairs perfectly with FastAPI's `response_model=UserRead` -- the framework
# calls model_validate under the hood, so this flag is what makes it work.
