"""
Don't double-validate
=====================
Once data is a BaseModel instance, it's already validated.
Re-running it through `model_validate(model_dump())` is pure waste.
"""

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    total: float


order = Order(id=1, customer="Alice", total=42.0)


# Anti-pattern: serialize -> dict -> re-validate. Two extra passes for nothing.
def bad(o: Order) -> Order:
    return Order.model_validate(o.model_dump())


# Better: pass the instance directly. Downstream functions should accept the model.
def good(o: Order) -> Order:
    return o


# If you really need a copy (e.g., to mutate without aliasing), use model_copy.
cloned = order.model_copy(update={"total": 50.0})
print(cloned)


# Rule of thumb:
# - Validate once, at the boundary (HTTP input, DB row, file).
# - After that, trust the types. Keep the instance alive through the call chain.
# - model_dump() is for output (JSON response, logging), not for round-tripping.
