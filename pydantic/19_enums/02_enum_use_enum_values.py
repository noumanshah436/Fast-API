"""
use_enum_values
===============
Dump the raw value instead of the enum instance.
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict


class Status(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Post(BaseModel):
    # Default behaviour: model_dump() returns Status.ACTIVE, an Enum object.
    title: str
    status: Status


p = Post(title="Hi", status="active")
print(p.model_dump())           # {'title': 'Hi', 'status': <Status.ACTIVE>}
print(p.model_dump()["status"]) # Status.ACTIVE  -- an enum instance


class PostFlat(BaseModel):
    # use_enum_values makes dumps return the raw string "active".
    # Useful when passing dicts straight to an ORM or a SQL driver
    # that doesn't know about Python Enum types.
    model_config = ConfigDict(use_enum_values=True)

    title: str
    status: Status


p2 = PostFlat(title="Hi", status="active")
print(p2.model_dump())          # {'title': 'Hi', 'status': 'active'}
print(type(p2.model_dump()["status"]))  # <class 'str'>
