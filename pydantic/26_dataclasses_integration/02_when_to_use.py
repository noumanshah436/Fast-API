"""
Pick one: BaseModel vs pydantic dataclass vs stdlib dataclass
=============================================================
Decision tree in one glance.

Question                                   -> Pick
-------------------------------------------------------------
Crossing an HTTP/JSON boundary?            -> BaseModel
Need model_json_schema / OpenAPI?          -> BaseModel
Need aliases, model_dump, validators?      -> BaseModel
Existing code uses dataclasses.fields()?   -> pydantic @dataclass
Third-party lib expects a dataclass?       -> pydantic @dataclass
Trusted internal data, no validation?      -> stdlib @dataclass

Why BaseModel wins by default: its API is a superset.
Pydantic dataclasses exist for interop, not for new designs.
"""

from dataclasses import fields
from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass


# Scenario 1: library helper iterates stdlib fields() -- BaseModel would not fit.
@pydantic_dataclass
class JobConfig:
    name: str
    retries: int = 3


def describe(obj):  # pretend this is third-party code
    return {f.name: getattr(obj, f.name) for f in fields(obj)}


print(describe(JobConfig(name="nightly-sync")))


# Scenario 2: HTTP boundary -- need schema + JSON serialization. BaseModel.
class JobRequest(BaseModel):
    name: str
    retries: int = 3


print(JobRequest(name="x").model_dump_json())
print(JobRequest.model_json_schema()["required"])
