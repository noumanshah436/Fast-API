"""
Required Fields
===============
No default == required. `Field(...)` makes it explicit AND attaches constraints.

Ways to say "required"
----------------------
name: str                          →  implicit required — no default
name: str = Field(..., min_length=1)  →  explicit required + constraint + schema description
                                       `...` (Ellipsis) is the "no default" sentinel

Error types you will see
------------------------
omitted                            →  type="missing"
wrong type                         →  type="int_parsing" / "string_type" / ...
constraint failure                 →  type="string_too_short" / "greater_than" / ...

Gotcha
------
A required field with a failed CONSTRAINT does not report as "missing".
"""

from pydantic import BaseModel, Field, ValidationError


class SignupForm(BaseModel):
    # Implicit required.
    email: str

    # Explicit required + constraint. Same requiredness as above, plus min_length.
    password: str = Field(..., min_length=8)

    # Same pattern, adds an OpenAPI description (FastAPI picks this up).
    username: str = Field(..., min_length=1, description="Display handle")


# Happy path — all three provided.
form = SignupForm(email="a@x.com", password="hunter22!", username="alice")
print(form)


# Missing field → "missing" error, distinct from type errors.
try:
    SignupForm(email="a@x.com", password="hunter22!")
except ValidationError as e:
    err = e.errors()[0]
    print(err["type"], err["loc"])   # missing ('username',)


# Constraint violation — the field was PRESENT, so "missing" is not the right label.
try:
    SignupForm(email="a@x.com", password="short", username="alice")
except ValidationError as e:
    print(e.errors()[0]["type"])     # string_too_short
