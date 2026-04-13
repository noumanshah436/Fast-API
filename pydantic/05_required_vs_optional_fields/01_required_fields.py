"""
Required Fields
===============
No default == required. Field(...) adds constraints without changing that.
"""

from pydantic import BaseModel, Field, ValidationError


class SignupForm(BaseModel):
    # No default -> required. Omitting it raises ValidationError(type="missing").
    email: str

    # Field(...) explicitly marks "required" and attaches constraints.
    # The Ellipsis is a sentinel meaning "no default, do not skip".
    password: str = Field(..., min_length=8)

    # Equivalent to the above but reads differently -- useful when you want
    # a description in the OpenAPI schema but still need "required".
    username: str = Field(..., min_length=1, description="Display handle")


# Happy path.
form = SignupForm(email="a@x.com", password="hunter22!", username="alice")
print(form)


# Missing field -> "missing" error, distinct from a type error.
try:
    SignupForm(email="a@x.com", password="hunter22!")
except ValidationError as e:
    err = e.errors()[0]
    print(err["type"], err["loc"])   # missing ('username',)


# Constraint violation -- required + too short fails on the constraint, not "missing".
try:
    SignupForm(email="a@x.com", password="short", username="alice")
except ValidationError as e:
    print(e.errors()[0]["type"])     # string_too_short
