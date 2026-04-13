"""
include / exclude
=================
Trim the output -- hide sensitive fields, send partial updates.
"""

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    bio: str | None = None


u = User(id=1, email="a@x.com", password_hash="xxx")

# Drop secrets before returning from an API handler.
print(u.model_dump(exclude={"password_hash"}))

# Whitelist mode: only these fields go out.
print(u.model_dump(include={"id", "email"}))

# exclude_none: skip fields whose value is None -- common for sparse responses.
print(u.model_dump(exclude_none=True))  # bio is dropped

# exclude_unset: only fields the caller actually set -- PATCH endpoints.
patch = User(id=1, email="a@x.com", password_hash="xxx")
print(patch.model_dump(exclude_unset=True))  # bio omitted -- never supplied

# Nested exclude uses dict syntax: exclude={"address": {"country"}}.
