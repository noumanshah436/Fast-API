"""
Factory pattern for fixtures
============================
Models with many required fields make tests noisy. A tiny factory keeps
each test focused on the one field it actually cares about.
"""

from typing import Any
import pytest
from pydantic import BaseModel, ValidationError, field_validator


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    country: str

    @field_validator("age")
    @classmethod
    def adult_only(cls, v: int) -> int:
        if v < 18:
            raise ValueError("Must be 18+")
        return v


# The baseline is *always valid*. Tests override only what they exercise.
def make_user(**overrides: Any) -> User:
    defaults: dict[str, Any] = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "country": "US",
    }
    return User(**{**defaults, **overrides})


def test_baseline_is_valid():
    u = make_user()
    assert u.name == "Alice"


def test_age_rule_rejects_minors():
    # Only the field under test appears in the call -- signal, no noise.
    with pytest.raises(ValidationError):
        make_user(age=15)


def test_can_override_multiple():
    u = make_user(name="Bob", country="UK")
    assert u.name == "Bob" and u.country == "UK"


# Scale this up: one factory per aggregate (User, Order, Invoice, ...).
# Keeps tests readable even as models grow to 20+ fields.
