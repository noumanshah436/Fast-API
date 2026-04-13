"""
Create / Update / Response split
================================
One domain entity, three Pydantic views — the standard FastAPI layout.

Per-view field matrix
---------------------
Field         Base    Create   Update (PATCH)   Response
-----------------------------------------------------------
email          yes    yes      optional         yes
full_name      yes    yes      optional         yes
password       -      yes      optional         NEVER
id             -      -        -                yes (server)
created_at     -      -        -                yes (server)

Rules of thumb:
- Shared fields live on a `*Base` class
- `Create` adds write-only secrets (passwords, tokens)
- `Update` makes every field Optional for PATCH semantics
- `Response` adds server-assigned fields + `from_attributes=True`
- For PATCH, serialize with `model_dump(exclude_unset=True)`

Gotchas:
- v2 does NOT auto-default `Optional[X]` to `None` -- write `= None` yourself
- Don't subclass `UserBase` for Update: inherited required fields stay required
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str                          # accepted on create only


class UserUpdate(BaseModel):
    # Not inheriting Base -- we want every field optional for PATCH.
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


print(UserCreate(email="a@x.io", full_name="Ann", password="hunter2").model_dump())

# exclude_unset -> only fields the client actually sent (true PATCH).
print(UserUpdate(full_name="Ann B.").model_dump(exclude_unset=True))

print(UserResponse(id=1, email="a@x.io", full_name="Ann",
                   created_at=datetime.now(timezone.utc)).model_dump())
