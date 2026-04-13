"""
Pydantic v1 vs v2
=================
v2 is a Rust-powered rewrite (pydantic-core). Same mental model, new API names.
Most tutorials online still show v1 -- this file is the cheat sheet.

Old (v1)                              →  New (v2)
---------------------------------------------------------------------------
m.dict()                              →  m.model_dump()
m.json()                              →  m.model_dump_json()
m.copy()                              →  m.model_copy()
Model.parse_obj(d)                    →  Model.model_validate(d)
Model.parse_raw(s)                    →  Model.model_validate_json(s)
Model.schema()                        →  Model.model_json_schema()
Model.construct(...)                  →  Model.model_construct(...)

class Config: ...                     →  model_config = ConfigDict(...)
  allow_population_by_field_name      →    populate_by_name
  orm_mode                            →    from_attributes
  anystr_strip_whitespace             →    str_strip_whitespace

@validator("x")                       →  @field_validator("x", mode="after")
@root_validator                       →  @model_validator(mode="after")

Behavior changes:
- Stricter coercion (e.g. float→int that loses precision is rejected)
- `Optional[X]` no longer auto-defaults to None -- write `= None` yourself
- Required-nullable is explicit: `x: int | None` still REQUIRED; add `= None`
- 5-50x faster thanks to Rust core
"""

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, field_validator


class User(BaseModel):
    id: int
    name: str
    # timezone-aware UTC; datetime.utcnow() is deprecated in Python 3.12+.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


u = User(id=1, name="Alice")

# Instance methods (renamed)
u.model_dump()
u.model_dump_json()
u.model_copy()

# Class methods (renamed)
User.model_validate({"id": 1, "name": "Alice"})
User.model_validate_json('{"id":1,"name":"Alice"}')
User.model_json_schema()
User.model_construct(id=1, name="Alice")  # skips validation -- use with care


# Config: inner class -> model_config dict
class Product(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )
    sku: str


# Validators: decorator + mode are explicit now
class SignUp(BaseModel):
    email: str

    @field_validator("email", mode="after")
    @classmethod
    def lowercase(cls, v: str) -> str:
        return v.lower()


print(u.model_dump())
