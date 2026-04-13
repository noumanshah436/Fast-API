"""
from_attributes — validate ORM-like objects
===========================================
v2's replacement for v1 `orm_mode`. Lets Pydantic read fields from object
attributes (getattr) instead of dict keys.

v1 vs v2
--------
v1                                   v2
-------------------------------------------------------------
class Config: orm_mode = True        model_config = ConfigDict(from_attributes=True)
Model.from_orm(row)                  Model.model_validate(row)

How lookup works:
- With `from_attributes=True`, `model_validate(obj)` reads `getattr(obj, field)`
- Missing attrs -> ValidationError, same as missing dict keys
- Nested models resolve through relationship attributes (e.g. `order.items`)

Gotchas:
- Fields absent from the schema are NEVER exposed — schema = security boundary
- Still works on plain dicts; `from_attributes=True` is additive
- SQLAlchemy lazy-loaded relationships trigger queries during validation
"""

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict


# Stand-in for a SQLAlchemy row -- any object with the right attrs qualifies.
class UserRow:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email
        self.created_at = datetime.now(timezone.utc)
        self.password_hash = "secret"  # intentionally NOT in the schema


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime
    # password_hash omitted -- schema excludes it, so it never leaks.


row = UserRow(id=1, email="alice@example.com")
print(UserOut.model_validate(row).model_dump())

# Dict input still works -- from_attributes doesn't forbid it.
print(UserOut.model_validate(
    {"id": 2, "email": "bob@x.io", "created_at": datetime.now(timezone.utc)}
))
