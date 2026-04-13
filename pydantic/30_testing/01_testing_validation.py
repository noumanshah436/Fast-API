"""
Testing validation with pytest
==============================
Two paths to cover: valid input constructs, invalid input raises.
"""

import pytest
from pydantic import BaseModel, ValidationError, field_validator


class User(BaseModel):
    id: int
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def has_at_sign(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v


# Happy path -- exercise type coercion and field access.
def test_user_valid():
    u = User(id="1", name="Alice", email="a@example.com")
    assert u.id == 1               # coerced from str
    assert u.name == "Alice"
    assert u.email == "a@example.com"


# Sad path -- bad type.
def test_user_rejects_bad_id():
    with pytest.raises(ValidationError):
        User(id="not-a-number", name="Alice", email="a@example.com")


# Sad path -- custom validator fires.
def test_user_rejects_bad_email():
    with pytest.raises(ValidationError):
        User(id=1, name="Alice", email="no-at-sign")


# Run with: pytest 01_testing_validation.py
