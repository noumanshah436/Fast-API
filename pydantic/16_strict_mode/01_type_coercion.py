"""
Default (lax) coercion
======================
v2 ships lax so messy external inputs (query strings, HTML forms) flow in
without hand-rolled parsing. Coercion is allowed only when it is lossless.

Target    Accepts beyond native
--------------------------------------------------------------------
int       "42", 42.0 (ONLY if the float is whole), True / False
float     "9.99", 10, True / False
bool      "true"/"false", "yes"/"no", "on"/"off", 0 / 1
str       real `str` only -- numbers are NOT auto-stringified
--------------------------------------------------------------------

Gotchas:
- `bool` coercion is the widest net: "1" -> True, "0" -> False.
- `int` takes "3.0" but rejects "3.5" -- lossy conversions always fail.
- Flip strict on for one call: `model_validate(data, strict=True)`.
  No model edits needed. Per-field / per-model levers live in file 02.
"""

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    in_stock: bool
    price: float


# Every value is a string -- simulates form-encoded or query-string input.
# Lax mode coerces each one to its declared native type for free.
p = Product(id="42", name="Book", in_stock="true", price="9.99")
print(p)

# One-shot strict: this call rejects coercion, the model itself remains lax.
# Ideal for a "trusted JSON boundary" where silent string->int would hide bugs.
try:
    Product.model_validate(
        {"id": "42", "name": "Book", "in_stock": "true", "price": "9.99"},
        strict=True,
    )
except Exception as e:
    print("strict call rejected:", type(e).__name__)
