"""
Overriding fields in subclasses
===============================
Redeclare a field in a subclass to tighten its type, constraints, or default.

Override rules
--------------
Action                     Allowed?   Notes
--------------------------------------------------------------
Tighten constraint          yes       `ge=0` -> `ge=100`
Change default              yes       can also change default_factory
Narrow type                 yes       `int | str` -> `int`
Widen type                  risky     may violate parent consumer's contract
Add new field               yes       subclass-only fields are fine
Remove inherited field      no        no native "drop" — use a sibling model

Gotchas:
- Overriding replaces the entire Field() -- repeat constraints you still need
- Validators inherit unless shadowed by a same-named subclass validator
- `model_config` merges: child overrides keys, parent keys still apply
"""

from pydantic import BaseModel, Field, ValidationError


class Item(BaseModel):
    name: str
    price: float = Field(ge=0)              # base: non-negative
    tags: list[str] = []


class PremiumItem(Item):
    # Tighter price floor. Re-declare type even though it's unchanged.
    price: float = Field(ge=100)

    # New default + min_length. Old default ([]) is gone -- overrides replace.
    tags: list[str] = Field(default_factory=lambda: ["premium"], min_length=1)

    # Subclass-only field.
    warranty_years: int = Field(ge=1, le=10)


print(Item(name="pen", price=1.5))

try:
    PremiumItem(name="watch", price=50, warranty_years=2)
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])       # price too low

print(PremiumItem(name="watch", price=250, warranty_years=3))
