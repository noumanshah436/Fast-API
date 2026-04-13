"""
Default (lax) type coercion
===========================
Pydantic converts compatible types so HTTP/form input "just works".
"""

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    in_stock: bool
    price: float


# Everything here is a string (as if pulled from a query string or form post).
p = Product(id="42", name="Book", in_stock="true", price="9.99")
print(p)
# id=42 name='Book' in_stock=True price=9.99

# Mental model: Pydantic accepts an input if there is an UNAMBIGUOUS
# conversion to the target type.
#   int    <- "42", 42.0 (if whole), True(=1)
#   float  <- "9.99", 10, True
#   bool   <- "true"/"false", "yes"/"no", "on"/"off", 0/1
#   str    <- (only str by default; ints are NOT stringified)

# Where it bites you: "1" becoming True, "0" becoming False, "3.0" becoming 3.
# If that is wrong for your domain -> use strict mode (next file).


# You can also opt into strict for a single call without touching the model:
try:
    Product.model_validate(
        {"id": "42", "name": "Book", "in_stock": "true", "price": "9.99"},
        strict=True,
    )
except Exception as e:
    print("strict call rejected lax input:", type(e).__name__)
