"""
@model_validator (mode="after")
===============================
Cross-field checks once every field has been validated.
"""

from datetime import date

from pydantic import BaseModel, ValidationError, model_validator


class Registration(BaseModel):
    password: str
    password_confirm: str

    # `self` here is a fully-built Registration; use it for field coupling.
    @model_validator(mode="after")
    def _passwords_match(self) -> "Registration":
        if self.password != self.password_confirm:
            raise ValueError("passwords do not match")
        return self


class Booking(BaseModel):
    start: date
    end: date

    @model_validator(mode="after")
    def _range_valid(self) -> "Booking":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self


print(Registration(password="hunter2", password_confirm="hunter2"))

try:
    Booking(start="2026-05-10", end="2026-05-01")
except ValidationError as e:
    print(e.errors()[0]["msg"])   # Value error, end must be after start


# Tip: prefer model_validator over field_validator whenever the rule needs
# MORE THAN ONE field -- it is clearer and avoids depending on field order.
