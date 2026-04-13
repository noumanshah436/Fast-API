"""
Required-Nullable vs Optional -- the PATCH pattern
==================================================
Two INDEPENDENT axes: nullability (type) and optionality (default).

                           None ok?   has default?   use case
----------------------------------------------------------------------------
x: str                     no         no             required, non-null
x: str | None              yes        no             PATCH: distinguish omit vs null
x: str | None = None       yes        yes            truly optional field
x: str = "x"               no         yes            required shape, safe default

PATCH semantics trick:
  key omitted   → "don't touch this column"
  value = None  → "set this column to NULL"
Use `model_dump(exclude_unset=True)` → drives the SQL UPDATE.
"""

from pydantic import BaseModel, ValidationError


class UserPatch(BaseModel):
    # Omit = leave alone; None = clear. Both keys optional-nullable.
    nickname: str | None = None
    bio: str | None = None


class UserReplace(BaseModel):
    # PUT-style: client MUST acknowledge every field -- required-nullable.
    nickname: str | None
    bio: str | None


# Only fields the caller actually set come out -- feeds a SQL UPDATE builder.
patch = UserPatch.model_validate({"bio": None})
print(patch.model_dump(exclude_unset=True))   # {'bio': None}

# PUT: omitting a field is an error, even though it's nullable.
try:
    UserReplace.model_validate({"nickname": "al"})
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])   # missing ('bio',)

print(UserReplace.model_validate({"nickname": "al", "bio": None}))
