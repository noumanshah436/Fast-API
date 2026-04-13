"""
ValidationError Structure
=========================
Pydantic collects EVERY error in one pass — no fail-fast surprises.

Each error dict
---------------
loc     →  tuple path, e.g. ("address", "zip_code")   — join with "." for API
msg     →  human-readable                             — show to end users
type    →  machine code, e.g. "missing", "int_parsing" — branch on this
input   →  the offending value                        — for logs / debugging
url     →  docs link for the error type               — optional

Useful methods
--------------
e.error_count()    →  int
e.errors()         →  list[dict]          (programmatic)
e.json(indent=2)   →  str (ready for 422) — FastAPI uses this shape internally
"""

from pydantic import BaseModel, ValidationError


class Address(BaseModel):
    street: str
    zip_code: int


class User(BaseModel):
    name: str
    age: int
    address: Address


# One payload, three independent problems — all reported together.
bad = {"age": "not-a-number", "address": {"street": "Main", "zip_code": "abc"}}

try:
    User.model_validate(bad)
except ValidationError as e:
    print("count:", e.error_count())
    for err in e.errors():
        # loc is a tuple so you can walk nested paths; join for display.
        path = ".".join(str(p) for p in err["loc"])
        print(f"  {path}: [{err['type']}] {err['msg']}  input={err['input']!r}")
