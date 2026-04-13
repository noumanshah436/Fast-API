"""
Field constraints
=================
Validate bounds and patterns declaratively -- no custom validators needed.
"""

from pydantic import BaseModel, Field, ValidationError


class Signup(BaseModel):
    # String bounds: enforce username/password policy at the edge.
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    # Regex pattern: only lowercase letters, digits, underscores.
    handle: str = Field(..., pattern=r"^[a-z0-9_]+$")
    # Numeric bounds: ge = >=, gt = >, le = <=, lt = <.
    age: int = Field(..., ge=13, le=120)
    # Useful for prices -- must be strictly positive.
    deposit: float = Field(..., gt=0)


ok = Signup(username="ada", password="secret123", handle="ada_l", age=30, deposit=10.0)
print(ok.model_dump())


# Each violation is reported separately -- great for form error UIs.
try:
    Signup(username="a", password="short", handle="BadHandle!", age=5, deposit=0)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
