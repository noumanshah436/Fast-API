"""
Pydantic dataclasses
====================
Same ergonomics as @dataclass, but fields are validated at init time.
"""

from dataclasses import asdict, fields, is_dataclass
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass


@pydantic_dataclass
class UserDC:
    id: int
    name: str
    is_active: bool = True


# Validation fires on construction, just like a BaseModel.
try:
    UserDC(id="not-an-int", name="x")
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])

u = UserDC(id="1", name="Alice")   # "1" is coerced to int, same as BaseModel
print(u)

# Serialization: no model_dump here. Use dataclasses.asdict.
print(asdict(u))

# It really IS a dataclass as far as stdlib is concerned.
print("is_dataclass:", is_dataclass(u))
print("fields:", [f.name for f in fields(u)])


# Compare with BaseModel for contrast.
class UserBM(BaseModel):
    id: int
    name: str
    is_active: bool = True


b = UserBM(id=1, name="Alice")
print(b.model_dump())              # richer API: model_dump, model_dump_json, etc.
print(b.model_json_schema()["properties"].keys())  # schema only on BaseModel
