from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import Body, FastAPI, Query, Path, Cookie, Header, status
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()


# Part 15 - Response Status Codes
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(pk: str):
    print("pk", pk)
    return pk


@app.get("/items/", status_code=status.HTTP_302_FOUND)
async def read_items_redirect():
    return {"hello": "world"}
