"""
Discriminated (tagged) unions
=============================
When payloads share a tag field, tell Pydantic which one to use.
Faster validation and sharp error messages.
"""

from typing import Literal, Annotated
from pydantic import BaseModel, Field, ValidationError


class Cat(BaseModel):
    type: Literal["cat"]        # Literal is the tag -- must be exactly "cat"
    meows: int


class Dog(BaseModel):
    type: Literal["dog"]
    barks: int


class Pet(BaseModel):
    # discriminator tells Pydantic: "look at `type` to pick the right model".
    # Without this, it would try each in turn -- slower and errors reference
    # every branch. With it, errors point at the specific mismatched shape.
    animal: Annotated[Cat | Dog, Field(discriminator="type")]


print(Pet(animal={"type": "cat", "meows": 5}))
print(Pet(animal={"type": "dog", "barks": 3}))

# Unknown tag -- error names the allowed discriminator values.
try:
    Pet(animal={"type": "fish", "bubbles": 2})
except ValidationError as e:
    print(e.errors()[0]["msg"])
