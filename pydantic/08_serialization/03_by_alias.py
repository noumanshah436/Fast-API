"""
by_alias on dump
================
Keep Python snake_case internally; emit camelCase JSON to the client.

Call                              Output keys
--------------------------------------------------
m.model_dump()                    Python attribute names
m.model_dump(by_alias=True)       Field alias (camelCase / wire format)
m.model_dump_json(by_alias=True)  JSON string with aliases

FastAPI pattern: accept AND return `by_alias=True` so the wire contract is
independent of whatever the Python code happens to name things.
"""

from pydantic import BaseModel, ConfigDict, Field


class OrderResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: int = Field(..., alias="orderId")
    customer_name: str = Field(..., alias="customerName")
    total_usd: float = Field(..., alias="totalUsd")


order = OrderResponse(order_id=42, customer_name="Ada", total_usd=99.9)

print(order.model_dump())                  # Python names -- internal logs
print(order.model_dump(by_alias=True))     # camelCase -- client response
print(order.model_dump_json(by_alias=True))
