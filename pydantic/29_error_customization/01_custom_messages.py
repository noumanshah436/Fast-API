"""
Custom error messages
=====================
Raise ValueError inside a validator -- the message lands in ValidationError.
"""

from pydantic import BaseModel, ValidationError, field_validator


class SignupForm(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_lowercase(cls, v: str) -> str:
        # Business rule: usernames must be lowercase. Speak the user's language.
        if v != v.lower():
            raise ValueError("Username must be lowercase")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v


try:
    SignupForm(username="Alice", password="short")
except ValidationError as e:
    for err in e.errors():
        # loc = ("username",), msg = "Value error, Username must be lowercase"
        print(err["loc"], "->", err["msg"])


# Notes:
# - Pydantic prefixes the message with "Value error, " in err["msg"].
#   Use err["ctx"]["error"] or strip the prefix if you want just your text.
# - Keep messages actionable: tell the user what to fix, not what's wrong internally.
