"""
Serializing enums
=================
Default output is the enum VALUE. Override to emit the NAME, or anything else.

Cheat sheet
---------------------------------------------------------------------------
Default behavior     model_dump -> Enum member; JSON -> .value
Emit .name           @field_serializer(...) -> v.name
Emit int / alt repr  @field_serializer(...) -> custom mapping
use_enum_values=True (ConfigDict) -> dump always uses .value directly

Picking the right output
- Machine-to-machine APIs     → .value (stable, lowercase, snake-friendly)
- Admin UIs / logs / humans   → .name (SCREAMING_CASE, self-describing)
- Legacy integrations         → map to your own scheme in the serializer
"""

from enum import Enum

from pydantic import BaseModel, field_serializer


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class AccountDefault(BaseModel):
    role: Role


# Default: JSON -> {"role":"admin"} (the value).
print(AccountDefault(role=Role.ADMIN).model_dump_json())


class AccountNamed(BaseModel):
    role: Role

    # Contract says "ADMIN"/"USER" in responses, not the lowercase values.
    @field_serializer("role")
    def _ser_role(self, v: Role) -> str:
        return v.name


print(AccountNamed(role=Role.ADMIN).model_dump())        # {'role': 'ADMIN'}
print(AccountNamed(role=Role.GUEST).model_dump_json())   # {"role":"GUEST"}
