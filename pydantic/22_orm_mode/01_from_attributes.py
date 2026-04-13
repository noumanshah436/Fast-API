"""
from_attributes: validate ORM-like objects
==========================================
v2 replaces v1's `orm_mode`. Same idea: read fields from attrs, not dict keys.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Stand-in for a SQLAlchemy row -- any object exposing the right attributes works.
class UserRow:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email
        self.created_at = datetime(2026, 1, 1)
        self.password_hash = "secret"  # intentionally NOT exposed by the schema


class UserOut(BaseModel):
    # Tell Pydantic it's OK to pull data from object attributes.
    # Without this flag, model_validate(orm_obj) raises a type error.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime
    # password_hash is omitted -- the schema is also a security boundary.


row = UserRow(id=1, email="alice@example.com")

# Use model_validate (v1 was `from_orm`). It walks attributes by field name.
user = UserOut.model_validate(row)
print(user.model_dump())

# The reverse (dict -> model) still works; from_attributes is additive.
print(UserOut.model_validate({"id": 2, "email": "bob@x.io",
                              "created_at": datetime.now()}))
