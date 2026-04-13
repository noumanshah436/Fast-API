"""
Pydantic vs dataclasses
=======================
Both use type hints. Only Pydantic enforces them at runtime.

                        @dataclass          BaseModel (Pydantic)
-------------------------------------------------------------------
Runtime type check      none                full validation
Coercion ("1" → 1)      no                  yes (lax by default)
Bad input               silently stored     ValidationError
JSON in                 json.loads + **     model_validate_json()
JSON out                manual asdict       model_dump_json()
JSON Schema             none                model_json_schema()
Speed                   fastest (no work)   Rust core, 5–50× v1

Rule of thumb
-------------
- @dataclass  → internal, trusted, hot-path structs
- BaseModel   → boundaries: HTTP, config, files, third-party APIs
"""

from dataclasses import dataclass
from pydantic import BaseModel, ValidationError


@dataclass
class UserDC:
    id: int
    name: str


# Dataclasses trust you — hints are documentation, not enforcement.
bad = UserDC(id="not an int", name=123)
print("dataclass accepted:", bad)


class UserPD(BaseModel):
    id: int
    name: str


try:
    UserPD(id="not an int", name=123)
except ValidationError as e:
    # Pydantic catches what dataclass would silently accept.
    print("pydantic rejected:", e.errors()[0]["msg"])

# Use dataclasses for internal, trusted data structures.
# Use Pydantic at boundaries -- HTTP payloads, config, external files.
