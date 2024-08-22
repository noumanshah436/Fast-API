from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    Depends,
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

# Dependencies in FastAPI are very powerful. They allow us to do things like handle user authentication and 
# authorization, abstract out duplicated code, and fetch a database session, among other things.

# In this video I give you an introduction on how to use Dependencies in FastAPI.


# Part 22 - Dependencies Intro
async def hello():
    return "world"


async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


# we can also nest dependencies like this:

# async def common_parameters(
#     q: str | None = None, skip: int = 0, limit: int = 100, blah: str = Depends(hello)
# ):
#     return {"q": q, "skip": skip, "limit": limit, "hello": blah}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
