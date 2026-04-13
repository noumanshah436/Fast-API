"""
@field_serializer
=================
Control how individual fields are emitted.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_serializer


class Invoice(BaseModel):
    number: str
    issued_at: datetime
    # Decimal keeps precision internally, but JSON has no Decimal type.
    amount: Decimal

    # Emit timestamps in a fixed ISO format (seconds precision, trailing Z).
    @field_serializer("issued_at")
    def _ser_issued_at(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Cast Decimal to str so clients never see it as a float and lose cents.
    @field_serializer("amount")
    def _ser_amount(self, v: Decimal) -> str:
        return f"{v:.2f}"


inv = Invoice(
    number="INV-001",
    issued_at=datetime(2026, 4, 13, 10, 30, 0),
    amount=Decimal("199.95"),
)

print(inv.model_dump())
# {'number': 'INV-001', 'issued_at': '2026-04-13T10:30:00Z', 'amount': '199.95'}

print(inv.model_dump_json())
# {"number":"INV-001","issued_at":"2026-04-13T10:30:00Z","amount":"199.95"}


# Tip: pass `when_used="json"` if you want the Python dict to keep the native
# Decimal / datetime objects and only stringify them in JSON output.
