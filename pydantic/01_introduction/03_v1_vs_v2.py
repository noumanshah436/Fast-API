"""
Pydantic v1 vs v2
=================
v2 renamed the main API. Tutorials online still show v1 -- know the mapping.
"""

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


u = User(id=1, name="Alice")

# v2 API (preferred, in use below)
u.model_dump()           # v1: u.dict()
u.model_dump_json()      # v1: u.json()
User.model_validate({"id": 1, "name": "Alice"})        # v1: User.parse_obj(...)
User.model_validate_json('{"id": 1, "name": "Alice"}') # v1: User.parse_raw(...)
User.model_json_schema()                                # v1: User.schema()


# Config also changed: inner `class Config` -> `model_config` dict.
class Product(BaseModel):
    model_config = {"extra": "forbid", "str_strip_whitespace": True}
    sku: str


# Decorators changed too:
#   @validator       -> @field_validator
#   @root_validator  -> @model_validator
# v2 is a Rust rewrite -- 5-50x faster, stricter by default.
print(u.model_dump())
