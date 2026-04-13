"""
String constraints via Annotated + Field
========================================
Preferred Pydantic v2 style for constraining strings.
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError


class SignUp(BaseModel):
    # Annotated keeps the type readable; Field attaches the validation rules.
    # Pattern ensures lowercase letters only -- catches typos before DB insert.
    username: Annotated[str, Field(min_length=3, max_length=20, pattern=r"^[a-z]+$")]

    # strip_whitespace prevents sneaky padding in emails / logins.
    email: Annotated[str, Field(min_length=5, strip_whitespace=True)]


# Valid input.
print(SignUp(username="alice", email="  a@b.co  "))  # email gets stripped

# Too short, wrong pattern -- raised together in one ValidationError.
try:
    SignUp(username="Al1", email="x")
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
