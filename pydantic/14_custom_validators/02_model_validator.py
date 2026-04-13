"""
@model_validator (mode="after")
===============================
Cross-field rules that run once every individual field has been validated.

Cheat sheet
---------------------------------------------------------------------------
@model_validator(mode="after")      self is the built model (use self.x)
@model_validator(mode="before")     data is the raw dict (pre-type)
@model_validator(mode="wrap")       advanced: call handler manually
return self (after)  /  return data (before)

Reach for @model_validator when
- The rule depends on 2+ fields (start < end, password == confirm).
- You want the check AFTER every field is already the right type.
- Prefer it over @field_validator for anything multi-field -- clearer and
  avoids fragile field-ordering assumptions.
"""

from datetime import date

from pydantic import BaseModel, ValidationError, model_validator


class Registration(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def _passwords_match(self) -> "Registration":
        if self.password != self.password_confirm:
            raise ValueError("passwords do not match")
        return self   # must return self in mode="after"


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
    print(e.errors()[0]["msg"])
