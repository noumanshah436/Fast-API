"""
Extending and overriding fields in subclasses
=============================================
Redeclare a field to tighten its type or constraints; add new fields freely.
"""

from pydantic import BaseModel, Field, ValidationError


class Item(BaseModel):
    name: str
    price: float = Field(ge=0)          # base constraint: non-negative
    tags: list[str] = []


class PremiumItem(Item):
    # Override: premium items must cost at least 100. Type stays float.
    price: float = Field(ge=100)

    # Override type: tags become a fixed, validated set of strings.
    tags: list[str] = Field(default_factory=lambda: ["premium"], min_length=1)

    # New field -- only exists on the subclass.
    warranty_years: int = Field(ge=1, le=10)


# Base still accepts a cheap item.
print(Item(name="pen", price=1.5))

# Subclass rejects a cheap price thanks to the tighter constraint.
try:
    PremiumItem(name="watch", price=50, warranty_years=2)
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])

# Subclass accepts when all constraints pass.
print(PremiumItem(name="watch", price=250, warranty_years=3))
