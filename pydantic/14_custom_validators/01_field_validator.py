"""
@field_validator (mode="after")
===============================
Single-field domain rules, AFTER type coercion has run.
"""

from pydantic import BaseModel, ValidationError, field_validator

RESERVED = {"admin", "root", "system"}


class Signup(BaseModel):
    username: str
    email: str

    # mode="after" (default): `v` is already guaranteed to be a str here.
    @field_validator("username", mode="after")
    @classmethod
    def _username_not_reserved(cls, v: str) -> str:
        if v.lower() in RESERVED:
            # ValueError becomes a ValidationError with loc=("username",).
            raise ValueError(f"{v!r} is reserved")
        return v

    @field_validator("email", mode="after")
    @classmethod
    def _email_lowercase(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        # Return the normalized value -- Pydantic uses whatever you return.
        return v.lower()


print(Signup(username="alice", email="Alice@Example.COM"))
# email is normalized to 'alice@example.com'

try:
    Signup(username="admin", email="a@b.co")
except ValidationError as e:
    print(e.errors()[0]["msg"])   # Value error, 'admin' is reserved
