"""
Basic inheritance: Create / Update / Response split
===================================================
One base model, three views -- the workhorse pattern in FastAPI apps.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    # Fields shared by every view of a user.
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    # Password is accepted on create only -- never echoed back.
    password: str


class UserUpdate(BaseModel):
    # PATCH semantics: every field optional, no inheritance of required ones.
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    # Server-assigned fields only appear on the way out.
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# Demo
create = UserCreate(email="a@x.io", full_name="Ann", password="hunter2")
print("create:", create.model_dump())

patch = UserUpdate(full_name="Ann B.")
# exclude_unset keeps PATCH minimal -- only fields the client actually sent.
print("patch :", patch.model_dump(exclude_unset=True))

resp = UserResponse(id=1, email="a@x.io", full_name="Ann",
                    created_at=datetime(2026, 4, 13))
print("resp  :", resp.model_dump())
