"""
Parsing dicts into models
=========================
`Model(**d)` and `Model.model_validate(d)` run the SAME pipeline — pick for readability.

Quick chooser
-------------
Model(**d)                  →  known-shape dict, reads like a constructor call
Model.model_validate(d)     →  dynamic / deeply-nested input
                               ALSO required when keys aren't valid Python idents
                               ALSO required with from_attributes=True (ORM rows)

Both paths
----------
- Apply the same lax coercion rules
- Raise the same ValidationError shape
- Track `exclude_unset` identically

Rule of thumb
-------------
Writing a test / hand-rolling args?   → constructor
Processing external / dynamic data?   → model_validate  (verb makes intent obvious)
"""

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    total: float


# Typical source: a DB row, a decoded JSON payload, forwarded kwargs.
row = {"id": 101, "customer": "Alice", "total": 42.5}

o1 = Order(**row)                  # constructor style
o2 = Order.model_validate(row)     # explicit "this is validation"

# Same pipeline → equal instances.
assert o1 == o2
print(o1.model_dump())
