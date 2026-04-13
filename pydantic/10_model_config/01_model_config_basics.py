"""
model_config basics
===================
Per-model behavior lives in ONE place: `model_config = ConfigDict(...)`.
v1's inner `class Config:` block is gone.

Flag                         Effect                                  Typical use
----------------------------------------------------------------------------------
str_strip_whitespace=True    trim leading/trailing spaces on strs    forms, CSV input
validate_assignment=True     re-run validation on attribute writes   long-lived models
frozen=True                  block all mutation (hashable!)          value objects, dict keys
populate_by_name=True        accept alias AND python name on input   snake/camel bridging
from_attributes=True         read via getattr (ORM rows)             SQLAlchemy → response
extra="ignore"/"forbid"/...  unknown-key policy                      see 02_extra_fields.py

Why a TypedDict? ConfigDict is typed -- IDEs autocomplete keys and flag typos
that v1's plain `class Config` never caught.
"""

from pydantic import BaseModel, ConfigDict, ValidationError


class StrictUser(BaseModel):
    # ConfigDict gives editor support + mypy-friendly typing.
    model_config = ConfigDict(
        str_strip_whitespace=True,   # "  Ada  " → "Ada" automatically
        validate_assignment=True,    # `user.name = "..."` runs the validator again
        frozen=False,                # flip to True for immutable value objects
    )

    id: int
    name: str


u = StrictUser(id=1, name="  Ada  ")
print(repr(u.name))   # 'Ada' -- whitespace trimmed on the way in

# With validate_assignment, post-construction mutations are validated too --
# catches bad writes that would otherwise silently corrupt state.
try:
    u.id = "not an int"
except ValidationError as e:
    print("assignment rejected:", e.errors()[0]["msg"])


# Legacy v1 form (shown for migration awareness only -- do NOT use):
# class OldUser(BaseModel):
#     class Config:
#         allow_population_by_field_name = True
# v2 equivalent:
#     model_config = ConfigDict(populate_by_name=True)
