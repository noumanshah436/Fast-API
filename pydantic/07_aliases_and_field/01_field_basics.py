"""
Field basics
============
Attach metadata (description, title, examples) to fields for schema + docs.
"""

from pydantic import BaseModel, Field


class Product(BaseModel):
    # description/title feed into OpenAPI / FastAPI auto-docs.
    id: int = Field(..., title="Product ID", description="Primary key from DB")
    name: str = Field(..., description="Human-readable product name")
    # default value + example for API docs.
    in_stock: bool = Field(default=True, description="Whether item is purchasable")
    price: float = Field(..., examples=[9.99, 19.99])


p = Product(id=1, name="Keyboard", price=49.99)
print(p.model_dump())

# The schema is what FastAPI uses to generate /docs.
schema = Product.model_json_schema()
print(schema["properties"]["id"])
# {'description': 'Primary key from DB', 'title': 'Product ID', 'type': 'integer'}
