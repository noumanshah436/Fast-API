"""
Pydantic dataclass vs BaseModel: which to pick?
===============================================
Rule of thumb: BaseModel unless you need dataclass interop.
"""

from dataclasses import asdict, fields
from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass


# Scenario 1: third-party code iterates dataclasses.fields(obj).
# A pydantic dataclass slots right in; a BaseModel would not.
@pydantic_dataclass
class JobConfig:
    name: str
    retries: int = 3


def describe(obj):
    # Hypothetical library helper that only understands dataclasses.
    return {f.name: getattr(obj, f.name) for f in fields(obj)}


print(describe(JobConfig(name="nightly-sync")))


# Scenario 2: HTTP boundary -- you want JSON schema, aliases, model_dump_json,
# validators, etc. BaseModel is the right tool.
class JobRequest(BaseModel):
    name: str
    retries: int = 3


print(JobRequest(name="x").model_dump_json())
print(JobRequest.model_json_schema()["required"])


# Quick guide:
#   BaseModel           -> APIs, config, anything touching JSON or OpenAPI.
#   pydantic dataclass  -> validation layer on top of existing dataclass code.
#   stdlib @dataclass   -> trusted internal data, no validation needed.
print(asdict(JobConfig(name="demo")))
