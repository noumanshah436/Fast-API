"""
Enum fields
===========
Pydantic accepts either the enum instance or its raw value as input.
"""

from enum import Enum
from pydantic import BaseModel, ValidationError


# Inherit from str so the value is natively JSON-serializable
# (no custom encoder needed) and compares equal to its string form.
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Account(BaseModel):
    username: str
    role: Role


# Either form is accepted -- handy for both Python callers and JSON payloads.
print(Account(username="alice", role=Role.ADMIN))
print(Account(username="bob", role="user"))

# model_dump() keeps enum instances by default.
print(Account(username="alice", role="admin").model_dump())
# model_dump_json() serializes the value -- "admin", not "Role.ADMIN".
print(Account(username="alice", role="admin").model_dump_json())

# Unknown value -> ValidationError listing allowed members.
try:
    Account(username="x", role="superuser")
except ValidationError as e:
    print(e.errors()[0]["msg"])
