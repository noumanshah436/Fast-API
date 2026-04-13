"""
@field_serializer
=================
Control how a single field is emitted by model_dump / model_dump_json.

Cheat sheet
---------------------------------------------------------------------------
@field_serializer("x")                            runs for dict AND JSON output
@field_serializer("x", when_used="json")          only for JSON (dict stays raw)
@field_serializer("x", when_used="unless-none")   skip when value is None
@field_serializer("x", "y")                       one function, many fields
@field_serializer("*")                            wildcard -- every field

Common real-world uses
- datetime  → fixed ISO format, epoch seconds, or locale-specific string
- Decimal   → stringify so JSON clients don't lose cents to float
- Enum      → emit .name instead of .value for human-facing APIs
- secrets   → mask ("****1234") before leaving the server
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_serializer


class Invoice(BaseModel):
    number: str
    issued_at: datetime
    amount: Decimal   # preserved internally; JSON has no Decimal type

    @field_serializer("issued_at")
    def _ser_issued_at(self, v: datetime) -> str:
        # Fixed contract: seconds precision, trailing Z -- no tz surprises.
        return v.strftime("%Y-%m-%dT%H:%M:%SZ")

    @field_serializer("amount")
    def _ser_amount(self, v: Decimal) -> str:
        # Emit as str so JSON keeps exact cents (floats lose precision).
        return f"{v:.2f}"


inv = Invoice(
    number="INV-001",
    issued_at=datetime(2026, 4, 13, 10, 30, 0),
    amount=Decimal("199.95"),
)
print(inv.model_dump_json())
# {"number":"INV-001","issued_at":"2026-04-13T10:30:00Z","amount":"199.95"}
