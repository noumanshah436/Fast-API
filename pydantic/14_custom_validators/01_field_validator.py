"""
@field_validator (mode="after")
===============================
Single-field domain rules AFTER type coercion has run.

Cheat sheet
---------------------------------------------------------------------------
@field_validator("x")                           default mode="after"
@field_validator("x", mode="before")            raw input, pre-type
@field_validator("x", "y")                      one rule, many fields
@field_validator("*")                           wildcard, every field
raise ValueError("...")                         -> ValidationError, loc=("x",)
return v (possibly transformed)                 Pydantic keeps what you return

Rules of thumb
- Need to RESHAPE input (str→list, trim) → mode="before".
- Need to VALIDATE/NORMALIZE a typed value → mode="after" (default).
- Cross-field logic → use @model_validator instead (next file).
- Always decorate with @classmethod; first arg is `cls`.
"""

from pydantic import BaseModel, ValidationError, field_validator

RESERVED = {"admin", "root", "system"}


class Signup(BaseModel):
    username: str
    email: str

    @field_validator("username")   # mode="after" by default
    @classmethod
    def _not_reserved(cls, v: str) -> str:
        if v.lower() in RESERVED:
            raise ValueError(f"{v!r} is reserved")
        return v

    @field_validator("email")
    @classmethod
    def _lowercase(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()   # normalized value flows downstream


print(Signup(username="alice", email="Alice@Example.COM"))

try:
    Signup(username="admin", email="a@b.co")
except ValidationError as e:
    print(e.errors()[0]["loc"], e.errors()[0]["msg"])
