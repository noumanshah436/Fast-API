from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

app = FastAPI()



## Part 21a - JSON Compatible Encoder
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": [],
    },
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items.get(item_id)


# update complete object
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    # jsonable_encoder =  Convert any object to something that can be encoded in JSON.
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# # update partial object
@app.patch("/items/{item_id}", response_model=Item)
def patch_item(item_id: str, item: Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    # exclude_unset -> only set items attributes that are passed and exclude that are not passed
    update_data = item.model_dump(exclude_unset=True)
    print("update_data", update_data)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item