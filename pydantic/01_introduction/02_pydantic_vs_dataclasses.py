"""
Pydantic vs dataclasses
=======================
Dataclasses give you typed containers. Pydantic gives you validation.
"""

from dataclasses import dataclass
from pydantic import BaseModel, ValidationError


@dataclass
class UserDC:
    id: int
    name: str


# dataclass accepts garbage at runtime -- type hints are ignored.
bad = UserDC(id="not an int", name=123)
print("dataclass accepted:", bad)  # no error, but data is wrong


class UserPD(BaseModel):
    id: int
    name: str


# Pydantic actually enforces the types.
try:
    UserPD(id="not an int", name=123)
except ValidationError as e:
    print("pydantic rejected:", e.errors()[0]["msg"])

# Use dataclasses for internal, trusted data structures.
# Use Pydantic at boundaries -- HTTP payloads, config, external files.
