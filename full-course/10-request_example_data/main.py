from enum import Enum

from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


# Part 10 - Declare Request Example Data
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 16.25,
    #             "tax": 1.67,
    #         }
    #     }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A __normal__ item works _correctly_",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 16.25,
                    "tax": 1.67,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {"name": "Bar", "price": "16.25"},
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "description": "Hello youtubers",
                "value": {"name": "Baz", "price": "sixteen point two five"},
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
