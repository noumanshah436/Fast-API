"""
ValidationError Structure
=========================
Pydantic collects every error at once -- inspect loc / msg / type / input.
"""

from pydantic import BaseModel, ValidationError


class Address(BaseModel):
    street: str
    zip_code: int


class User(BaseModel):
    name: str
    age: int
    address: Address


# Bad payload with three separate problems -- missing field, bad int, nested int.
bad = {
    "age": "not-a-number",
    "address": {"street": "Main", "zip_code": "abc"},
    # "name" missing entirely
}

try:
    User.model_validate(bad)
except ValidationError as e:
    # error_count: quick check, useful for logging severity.
    print("errors:", e.error_count())

    # .errors() -> list of dicts, ideal for programmatic handling.
    # Each entry has: loc (tuple path), msg, type (machine code), input.
    for err in e.errors():
        print(f"  loc={err['loc']}  type={err['type']}  msg={err['msg']}")
        print(f"    input={err['input']!r}")

    # .json() -> ready-to-return string for API responses.
    # FastAPI uses this shape internally for 422 responses.
    print(e.json(indent=2))
