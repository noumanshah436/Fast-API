"""
Field constraints
=================
Declarative bounds -- no custom validators needed.

Numeric         Meaning      String / seq         Meaning
----------------------------------------------------------
gt              >            min_length           inclusive lower
ge              >=           max_length           inclusive upper
lt              <            pattern              regex (full match)
le              <=

All violations are reported individually -- perfect for form error UIs.
"""

from pydantic import BaseModel, Field, ValidationError


class Signup(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    handle: str = Field(..., pattern=r"^[a-z0-9_]+$")   # lowercase handle only
    age: int = Field(..., ge=13, le=120)
    deposit: float = Field(..., gt=0)                   # strictly positive price


print(Signup(username="ada", password="secret123", handle="ada_l",
             age=30, deposit=10.0).model_dump())

try:
    Signup(username="a", password="short", handle="BadHandle!", age=5, deposit=0)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
