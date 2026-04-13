"""
Required-Nullable vs Optional -- the PATCH pattern
==================================================
Two axes: can be None (type) and can be omitted (has default).
"""

from typing import Optional

from pydantic import BaseModel, ValidationError


# Classic PATCH body: the client sends only fields they want to change.
# "omitted" and "null" MUST mean different things:
#   - omitted -> leave DB column alone
#   - null    -> set DB column to NULL
# That needs a sentinel distinguishing "unset" from "set to None".
class UserPatch(BaseModel):
    # Optional + nullable: omit = "don't touch", None = "clear it".
    # The Optional import is shown here because this topic is about nullability;
    # `str | None = None` is equivalent and usually preferred in 3.10+.
    nickname: Optional[str] = None
    bio: str | None = None


# Required-nullable: must send the key explicitly, even if the value is null.
# Used when the API contract wants to force the client to acknowledge the field.
class UserReplace(BaseModel):
    nickname: str | None          # required, may be None
    bio: str | None               # required, may be None


# PATCH -- omit what you don't want to change, pass None to clear.
patch = UserPatch.model_validate({"bio": None})
# model_dump(exclude_unset=True) is the key trick: it returns ONLY fields the
# caller actually set. That's exactly what you want for a SQL UPDATE builder.
print(patch.model_dump(exclude_unset=True))   # {'bio': None}


# PUT/replace -- both fields must appear; omitting is an error.
try:
    UserReplace.model_validate({"nickname": "al"})
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])   # missing ('bio',)

# Both provided, one null -- fine.
replace = UserReplace.model_validate({"nickname": "al", "bio": None})
print(replace)
