"""
Parsing dicts into models
=========================
Model(**d) and model_validate(d) are equivalent -- pick for readability.
"""

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    total: float


# Typical source: a DB row fetched as a dict, a cached JSON decoded elsewhere,
# or kwargs forwarded from a higher-level function.
row = {"id": 101, "customer": "Alice", "total": 42.5}


# Constructor form -- use when the dict is known-shape and "spread" reads clean.
o1 = Order(**row)

# model_validate form -- use when the dict is dynamic, deeply nested,
# or you need the explicit "this is validation" signal at call sites.
# Also the only option when keys aren't valid Python identifiers.
o2 = Order.model_validate(row)

print(o1 == o2)            # True -- same validation pipeline under the hood
print(o1.model_dump())


# Why prefer model_validate in many codebases:
# - explicit verb: "validate", not "construct"
# - works with SQLAlchemy rows via from_attributes=True (not shown here)
# - no risk of accidentally passing extra kwargs that shadow a field
weird_keys = {"id": 1, "customer": "Bob", "total": 9.99}
o3 = Order.model_validate(weird_keys)
print(o3)
