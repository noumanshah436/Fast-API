"""
Asserting on error details
==========================
Don't test the message text (it changes between versions).
Test the structured fields: `type` and `loc`.
"""

import pytest
from pydantic import BaseModel, ValidationError


class Account(BaseModel):
    id: int
    email: str
    balance: float


def test_missing_field_reported():
    with pytest.raises(ValidationError) as exc_info:
        Account(id=1, balance=0.0)  # email missing

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert errors[0]["loc"] == ("email",)


def test_wrong_type_reported():
    with pytest.raises(ValidationError) as exc_info:
        Account(id="abc", email="x@y.z", balance=0.0)

    errors = exc_info.value.errors()
    assert errors[0]["type"] == "int_parsing"   # stable identifier
    assert errors[0]["loc"] == ("id",)


# Why not assert on `msg`?
# - Pydantic's human-readable messages are not part of its stable API.
# - `type` strings ("missing", "int_parsing", "value_error", ...) are documented
#   and rarely change -- safer to assert against.
# - `loc` is how you prove the error attaches to the right field,
#   including nested paths like ("address", "zip").
