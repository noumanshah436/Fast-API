"""
Enum fields
===========
Fixed vocabularies with autocompletion, safe refactors, and free JSON schema.

Input accepted       Output (default)          Output (use_enum_values=True)
-----------------------------------------------------------------------------
Enum member or       model_dump() -> Enum      model_dump() -> raw value
its raw value        model_dump_json() -> val  model_dump_json() -> val
-----------------------------------------------------------------------------

Gotchas:
- Inherit from `str` (or `int`) so the value is natively JSON-serializable
  and compares equal to its string form -- no custom encoder required.
- Unknown values raise a `ValidationError` that lists the allowed members.
- `model_dump()` keeps the Enum instance by default; see 02 for the flat form.
"""

from enum import Enum
from pydantic import BaseModel, ValidationError


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Account(BaseModel):
    username: str
    role: Role


# Both forms are accepted -- convenient for Python callers AND JSON payloads.
print(Account(username="alice", role=Role.ADMIN))
print(Account(username="bob", role="user"))

# Default: dumps keep the Enum instance.
print(Account(username="alice", role="admin").model_dump())
# JSON dump serializes the raw value -- "admin", not "Role.ADMIN".
print(Account(username="alice", role="admin").model_dump_json())

# Unknown value -> ValidationError listing every allowed member.
try:
    Account(username="x", role="superuser")
except ValidationError as e:
    print(e.errors()[0]["msg"])
