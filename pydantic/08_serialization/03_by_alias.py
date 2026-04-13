"""
by_alias on dump
================
Emit camelCase JSON for frontends while keeping snake_case in Python.
"""

from pydantic import BaseModel, ConfigDict, Field


class OrderResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: int = Field(..., alias="orderId")
    customer_name: str = Field(..., alias="customerName")
    total_usd: float = Field(..., alias="totalUsd")


order = OrderResponse(order_id=42, customer_name="Ada", total_usd=99.9)

# Default dump uses Python names -- useful for internal logs / storage.
print(order.model_dump())
# {'order_id': 42, 'customer_name': 'Ada', 'total_usd': 99.9}

# by_alias=True is the shape you send back to a JS client.
print(order.model_dump(by_alias=True))
# {'orderId': 42, 'customerName': 'Ada', 'totalUsd': 99.9}

# Common FastAPI pattern: accept and return by_alias so the JSON contract is
# stable regardless of how Python code names things internally.
print(order.model_dump_json(by_alias=True))
