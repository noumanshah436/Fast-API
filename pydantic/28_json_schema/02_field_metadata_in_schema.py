"""
Field metadata in the schema
============================
`Field(description=..., examples=[...])` is not just for humans --
it ends up in the JSON Schema and in Swagger UI.
"""

import json
from pydantic import BaseModel, Field


class Product(BaseModel):
    sku: str = Field(
        description="Stock keeping unit, uppercase alphanumeric.",
        examples=["ABC-123", "WIDGET-42"],
        min_length=3,
        max_length=32,
    )
    price: float = Field(
        description="Price in USD, excluding tax.",
        examples=[9.99, 199.00],
        gt=0,
    )
    in_stock: bool = Field(default=True, description="Whether item is orderable now.")


schema = Product.model_json_schema()
print(json.dumps(schema["properties"]["sku"], indent=2))
# {
#   "description": "Stock keeping unit, uppercase alphanumeric.",
#   "examples": ["ABC-123", "WIDGET-42"],
#   "maxLength": 32,
#   "minLength": 3,
#   "title": "Sku",
#   "type": "string"
# }


# Why fill these in:
# - FastAPI's /docs renders description + examples next to each input field.
# - "Try it out" in Swagger pre-populates with your examples -> fewer support tickets.
# - Constraints (min_length, gt, ...) map to JSON Schema keywords for free.
