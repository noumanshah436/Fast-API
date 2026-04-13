"""
Field() basics
==============
Attach metadata to a type -- powers JSON schema, OpenAPI, FastAPI `/docs`.

Field arg                 Purpose                      Schema key
-----------------------------------------------------------------------
title                     short label                  "title"
description               long-form doc                "description"
examples                  sample values                "examples"
default / ...             default OR required marker   "default" / required list
alias                     wire-format name             property key
gt / ge / lt / le         numeric bounds               "exclusiveMinimum"...
min_length / max_length   length bounds                "minLength"/"maxLength"
pattern                   regex                        "pattern"

Rule of thumb:
- Plain `x: int = 0` is fine for 80% of fields.
- Reach for Field() the moment you need docs, constraints, aliases, or examples.
"""

from pydantic import BaseModel, Field


class Product(BaseModel):
    # `...` (ellipsis) marks the field required even with metadata attached.
    id: int = Field(..., title="Product ID", description="Primary key from DB")
    name: str = Field(..., description="Human-readable product name")
    in_stock: bool = Field(default=True, description="Whether item is purchasable")
    price: float = Field(..., examples=[9.99, 19.99])


p = Product(id=1, name="Keyboard", price=49.99)
print(p.model_dump())

# FastAPI /docs is literally this schema rendered as HTML.
print(Product.model_json_schema()["properties"]["id"])
