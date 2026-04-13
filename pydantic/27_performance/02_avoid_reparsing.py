"""
Don't double-validate
=====================
A BaseModel instance is already validated. Round-tripping it through
dump + validate is pure waste.

Anti-pattern                                What it costs
-------------------------------------------------------------------
Model.model_validate(obj.model_dump())      Full dump + full re-validate
Model(**obj.model_dump())                   Same, plus kwargs unpack
Revalidating on every function call         Death by a thousand passes

Do instead:
- Validate once at the boundary (HTTP in, DB row, file).
- Pass the *instance* through the call chain. Let types carry the trust.
- Need a mutation? -> model_copy(update={...}), not re-validate.
- model_dump() is for OUTPUT (JSON response, logs), not round-trips.
"""

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    total: float


order = Order(id=1, customer="Alice", total=42.0)


def bad(o: Order) -> Order:
    # Two extra passes for zero information gain.
    return Order.model_validate(o.model_dump())


def good(o: Order) -> Order:
    return o  # types already guarantee validity


# Need a tweaked copy without mutating the original? Use model_copy.
cloned = order.model_copy(update={"total": 50.0})
print(cloned)
