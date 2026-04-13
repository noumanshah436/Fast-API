"""
Allowing None
=============
`| None` widens the TYPE. It does NOT add a default -- that's separate.

Declaration                     Accepts None?   Required?   Mental model
-----------------------------------------------------------------------------
x: int                          no              yes         NOT NULL, required
x: int | None                   yes             yes         NULL ok, still required
x: int | None = None            yes             no          NULL ok, omittable
x: int = 0                      no              no          NOT NULL + default

Gotchas:
- `str | None` alone does NOT default to None -- caller still must send the key.
- Passing None to a non-nullable field raises `string_type` / `int_type` / etc.
- Mirror SQL: NULLABLE column → `T | None`; NOT NULL column → plain `T`.
"""

from pydantic import BaseModel, ValidationError


class DBUser(BaseModel):
    id: int                         # NOT NULL
    email: str                      # NOT NULL
    verified_at: str | None         # NULLABLE column, key still required
    deleted_at: str | None = None   # NULLABLE + omittable (safe default)


print(DBUser(id=1, email="a@x.com", verified_at=None).model_dump())
print(DBUser(id=2, email="b@x.com", verified_at="2025-01-01").verified_at)

# Sending None where the column is NOT NULL -- rejected at the edge, not in the DB.
try:
    DBUser(id=3, email=None, verified_at=None)
except ValidationError as e:
    print(e.errors()[0]["type"])    # string_type
