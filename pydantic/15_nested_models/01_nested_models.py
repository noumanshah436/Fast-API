"""
Nested models
=============
Compose BaseModels; nested dicts get deep-validated for free.
"""

from pydantic import BaseModel, ValidationError


class Customer(BaseModel):
    id: int
    name: str
    email: str


class Item(BaseModel):
    sku: str
    qty: int
    price: float


class Order(BaseModel):
    order_id: str
    customer: Customer      # nested model
    items: list[Item]       # list of nested models


# Typical API payload: one big dict. Pydantic validates every level.
payload = {
    "order_id": "ORD-42",
    "customer": {"id": 7, "name": "Alice", "email": "a@x.com"},
    "items": [
        {"sku": "A-1", "qty": "2", "price": "9.99"},   # strings coerced
        {"sku": "B-2", "qty": 1, "price": 19.50},
    ],
}

order = Order.model_validate(payload)
print(type(order.customer))       # <class ... Customer>
print(type(order.items[0]))       # <class ... Item>
print(order.items[0].qty + 1)     # 3  -- real int, not a string


# Errors point into the nested path so clients know exactly what to fix.
try:
    Order.model_validate({
        "order_id": "ORD-43",
        "customer": {"id": "not-int", "name": "B", "email": "b@x.com"},
        "items": [],
    })
except ValidationError as e:
    print(e.errors()[0]["loc"])   # ('customer', 'id')
