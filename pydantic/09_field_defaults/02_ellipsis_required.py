"""
Ellipsis = required
===================
Field(...) marks a field required explicitly -- needed when adding constraints.
"""

from pydantic import BaseModel, Field, ValidationError


class CreateUser(BaseModel):
    # You can't write `name: str = min_length=3` -- you need Field().
    # ... means "no default, this is required."
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    # Compare: age is optional (has a default).
    age: int | None = Field(default=None, ge=0, le=150)


ok = CreateUser(name="Ada", email="ada@example.com")
print(ok.model_dump())


# Missing required fields raises a clear error.
try:
    CreateUser(name="Ada")  # email missing
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])
    # missing ('email',)

# Note: `name: str` (no assignment) is ALSO required. Field(...) is preferred
# when you want the explicit marker next to constraints, to signal intent.
