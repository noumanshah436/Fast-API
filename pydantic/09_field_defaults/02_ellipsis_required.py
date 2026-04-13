"""
Ellipsis = required
===================
`Field(...)` means "no default, this field is required" -- the ellipsis is
the marker you need once constraints enter the picture.

Declaration                              Required?   Notes
-----------------------------------------------------------------------------
name: str                                yes         bare, no metadata
name: str = Field(...)                   yes         same, explicit marker
name: str = Field(..., min_length=3)     yes         required + constraint
name: str = Field(default="", ...)       no          default supplied
name: str | None = Field(default=None)   no          optional + nullable

Why `...`? You cannot write `name: str = min_length=3` -- you need Field().
Once you're using Field(), `...` is the only way to say "required."
"""

from pydantic import BaseModel, Field, ValidationError


class CreateUser(BaseModel):
    # Ellipsis keeps the field required while you attach validation rules.
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    # Contrast: age has default=None, so it's optional-nullable with a bound.
    age: int | None = Field(default=None, ge=0, le=150)


ok = CreateUser(name="Ada", email="ada@example.com")
print(ok.model_dump())


# Missing required field → clear, structured error pointing at the path.
try:
    CreateUser(name="Ada")   # email omitted
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])
    # missing ('email',)

# Note: `name: str` (no assignment) is ALSO required. Field(...) is preferred
# once constraints are present -- it keeps the "required" intent visible
# alongside the rules rather than hidden in the absence of an assignment.
