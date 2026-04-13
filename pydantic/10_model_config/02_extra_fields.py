"""
Extra fields policy
===================
Decide what happens when input contains keys you didn't declare.
"""

from pydantic import BaseModel, ConfigDict, ValidationError


class IgnoreModel(BaseModel):
    # Default -- unknown keys are silently dropped.
    model_config = ConfigDict(extra="ignore")
    id: int


class ForbidModel(BaseModel):
    # Raises -- use for request payloads where typos should surface loudly.
    model_config = ConfigDict(extra="forbid")
    id: int


class AllowModel(BaseModel):
    # Keeps unknown keys as attributes -- useful for pass-through / webhook envelopes.
    model_config = ConfigDict(extra="allow")
    id: int


payload = {"id": 1, "unexpected": "hello"}

print(IgnoreModel(**payload).model_dump())   # {'id': 1}  -- extra dropped

try:
    ForbidModel(**payload)
except ValidationError as e:
    print("forbid rejected:", e.errors()[0]["type"])  # 'extra_forbidden'

m = AllowModel(**payload)
print(m.model_dump())    # {'id': 1, 'unexpected': 'hello'}
print(m.unexpected)      # accessible as attribute
