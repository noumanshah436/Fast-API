"""
Numeric constraints
===================
Bounds and step rules, enforced at validation (and on assignment if enabled).

Kwarg          Meaning              Example
-----------------------------------------------------------
gt / ge        >  /  >=             gt=0  rejects 0 and below
lt / le        <  /  <=             le=100 allows 100
multiple_of    divisible by         multiple_of=0.01 (money cents)
allow_inf_nan  permit inf / NaN     False for DB-safe floats
-----------------------------------------------------------

Gotchas:
- `multiple_of` uses float math -- prefer `Decimal` for real-money logic.
- `gt=0` still accepts `True` (Python bool subclasses int) unless strict is on.
- Constraints flow into the generated JSON schema -- free API documentation.
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError


class Product(BaseModel):
    # gt=0 rules out free / negative prices; le acts as a sanity ceiling.
    price: Annotated[float, Field(gt=0, le=1_000_000)]
    # ge=1 -- you can't order zero items.
    quantity: Annotated[int, Field(ge=1)]
    # Ratio (not percent): clamp between 0 and 1.
    discount: Annotated[float, Field(ge=0, le=1)] = 0.0


print(Product(price=9.99, quantity=3, discount=0.1))

try:
    Product(price=-5, quantity=0, discount=1.5)
except ValidationError as e:
    # Each violated constraint becomes its own error entry.
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
