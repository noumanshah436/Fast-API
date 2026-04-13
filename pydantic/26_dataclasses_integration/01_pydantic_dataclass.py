"""
Pydantic dataclasses
====================
@pydantic.dataclasses.dataclass = stdlib @dataclass + runtime validation.

Feature                    stdlib @dataclass   pydantic @dataclass   BaseModel
--------------------------------------------------------------------------------
Validates at __init__      no                  yes                   yes
is_dataclass(obj)          True                True                  False
dataclasses.fields(obj)    works               works                 no
dataclasses.asdict(obj)    works               works                 no
.model_dump() / _json()    no                  no                    yes
.model_json_schema()       no                  no                    yes
Aliases / validators       no                  yes                   yes (richer)

Rule of thumb:
- BaseModel        -> APIs, JSON, OpenAPI. Default choice.
- pydantic dc      -> add validation to code that already uses dataclasses.
- stdlib dc        -> trusted internal data, no validation needed.
"""

from dataclasses import asdict, fields, is_dataclass
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass


@pydantic_dataclass
class UserDC:
    id: int
    name: str
    is_active: bool = True


# Validation fires on construction -- same as BaseModel.
try:
    UserDC(id="not-an-int", name="x")
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])

u = UserDC(id="1", name="Alice")   # "1" coerced to int
print(asdict(u))                    # no model_dump here -- use asdict
print(is_dataclass(u), [f.name for f in fields(u)])  # stdlib tools still work


# Contrast: BaseModel has the richer API.
class UserBM(BaseModel):
    id: int
    name: str


b = UserBM(id=1, name="Alice")
print(b.model_dump(), list(UserBM.model_json_schema()["properties"]))
