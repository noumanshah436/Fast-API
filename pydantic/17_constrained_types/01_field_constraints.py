"""
String constraints via Annotated + Field
========================================
Preferred v2 shape: base type stays readable, rules hang off it via Annotated.

Field kwarg               Effect
-----------------------------------------------------------------
min_length / max_length   length bounds
pattern                   regex (must fully match in v2)
strip_whitespace          trim input BEFORE length checks
to_lower / to_upper       normalize case before validating
-----------------------------------------------------------------

Gotchas:
- `pattern` anchors the full string -- explicit `^...$` is optional but harmless.
- `strip_whitespace` runs first, so "   " with `min_length=1` still fails.
- Every rule failure is collected into one ValidationError -- loop `e.errors()`.
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError


class SignUp(BaseModel):
    # The regex rejects uppercase letters and digits before the DB sees them.
    username: Annotated[str, Field(min_length=3, max_length=20, pattern=r"^[a-z]+$")]
    # Stripping defends against sneaky padding in logins / emails.
    email: Annotated[str, Field(min_length=5, strip_whitespace=True)]


print(SignUp(username="alice", email="  a@b.co  "))

try:
    SignUp(username="Al1", email="x")
except ValidationError as e:
    # All failures are reported together -- great for form-level error UI.
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
