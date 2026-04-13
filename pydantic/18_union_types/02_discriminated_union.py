"""
Discriminated (tagged) unions
=============================
When payloads already carry a tag (`type`, `kind`, `event`), let Pydantic
dispatch on it instead of trying every branch.

Plain union                  Discriminated union
-----------------------------------------------------------------
Try each member in turn      O(1) dispatch on the tag value
Error lists all branches     Error names the specific tag mismatch
Schema uses `anyOf`          Schema uses `oneOf` + discriminator map

Requirements:
- Every member has a `Literal[...]` field with a unique value.
- Declare the union as `Annotated[A | B, Field(discriminator="type")]`.

Gotchas:
- Missing / unknown tag -> error enumerates the allowed values.
- Discriminator field must exist on every member and be a `Literal`.
"""

from typing import Annotated, Literal
from pydantic import BaseModel, Field, ValidationError


class Cat(BaseModel):
    type: Literal["cat"]
    meows: int


class Dog(BaseModel):
    type: Literal["dog"]
    barks: int


class Pet(BaseModel):
    # discriminator="type" tells Pydantic which field to dispatch on.
    animal: Annotated[Cat | Dog, Field(discriminator="type")]


print(Pet(animal={"type": "cat", "meows": 5}))
print(Pet(animal={"type": "dog", "barks": 3}))

try:
    Pet(animal={"type": "fish", "bubbles": 2})
except ValidationError as e:
    # Clear error: unknown tag value, with the allowed set listed.
    print(e.errors()[0]["msg"])
