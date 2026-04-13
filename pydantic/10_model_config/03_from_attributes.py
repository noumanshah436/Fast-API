"""
from_attributes (ORM mode)
==========================
Build a Pydantic model from any object's attributes -- the SQLAlchemy case.
"""

from pydantic import BaseModel, ConfigDict


# Stand-in for a SQLAlchemy row / ORM object.
class UserORM:
    def __init__(self, id: int, email: str, is_admin: bool):
        self.id = id
        self.email = email
        self.is_admin = is_admin


class UserRead(BaseModel):
    # from_attributes=True tells Pydantic to read via getattr, not dict keys.
    # (v1 called this orm_mode=True.)
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_admin: bool


row = UserORM(id=1, email="ada@example.com", is_admin=False)

# model_validate walks the object's attributes and builds the model.
user = UserRead.model_validate(row)
print(user.model_dump())
# {'id': 1, 'email': 'ada@example.com', 'is_admin': False}

# Typical FastAPI flow: DB query -> ORM row -> response_model=UserRead.
# Without from_attributes, Pydantic would expect a dict and complain.
