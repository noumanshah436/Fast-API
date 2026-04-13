"""
Numeric constraints
===================
gt, ge, lt, le, multiple_of -- enforced at validation time.
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError


class Product(BaseModel):
    # gt=0 rejects free/negative prices; le=1_000_000 is a sanity ceiling.
    price: Annotated[float, Field(gt=0, le=1_000_000)]

    # ge=1 because you can't order zero items; multiple_of=1 keeps it integral.
    quantity: Annotated[int, Field(ge=1, multiple_of=1)]

    # Discount between 0 and 1 inclusive -- a ratio, not a percentage.
    discount: Annotated[float, Field(ge=0, le=1)] = 0.0


print(Product(price=9.99, quantity=3, discount=0.1))

# Negative price is caught before it hits the pricing engine.
try:
    Product(price=-5, quantity=0, discount=1.5)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
