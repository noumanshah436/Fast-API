"""
Serializing enums
=================
Default = enum value. Override to emit the name, or anything else.
"""

from enum import Enum

from pydantic import BaseModel, field_serializer


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class AccountDefault(BaseModel):
    role: Role


# By default Pydantic serializes the enum's VALUE.
print(AccountDefault(role=Role.ADMIN).model_dump())
# {'role': <Role.ADMIN: 'admin'>}  -> JSON becomes {"role": "admin"}


class AccountNamed(BaseModel):
    role: Role

    # Useful when your API contract says "ADMIN", "USER" (SCREAMING_CASE names)
    # rather than the lowercase values stored internally.
    @field_serializer("role")
    def _ser_role(self, v: Role) -> str:
        return v.name


print(AccountNamed(role=Role.ADMIN).model_dump())   # {'role': 'ADMIN'}
print(AccountNamed(role=Role.GUEST).model_dump_json())  # {"role":"GUEST"}


# Rule of thumb:
#   - API consumed by other services  -> emit VALUE (stable, machine-friendly).
#   - Human-facing logs / admin UIs   -> emit NAME.
