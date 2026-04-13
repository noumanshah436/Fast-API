"""
model_config basics
===================
v2 uses ConfigDict at class level. v1's inner `class Config` is gone.
"""

from pydantic import BaseModel, ConfigDict, ValidationError


class StrictUser(BaseModel):
    # ConfigDict is a TypedDict -- editor autocomplete + type-checking.
    model_config = ConfigDict(
        str_strip_whitespace=True,   # trim whitespace on str fields
        validate_assignment=True,    # re-validate when you do user.name = "..."
        frozen=False,                # set True for immutable models
    )

    id: int
    name: str


u = StrictUser(id=1, name="  Ada  ")
print(repr(u.name))  # 'Ada' -- auto-stripped

# With validate_assignment, mutations are validated too.
try:
    u.id = "not an int"
except ValidationError as e:
    print("assignment rejected:", e.errors()[0]["msg"])


# v1 style (DON'T use) for reference:
# class OldUser(BaseModel):
#     class Config:
#         allow_population_by_field_name = True
# -> in v2 it's `model_config = ConfigDict(populate_by_name=True)`
