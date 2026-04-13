"""
default_factory basics
======================
Fresh mutable defaults, one per instance.
"""

from pydantic import BaseModel, Field


class Cart(BaseModel):
    # Every Cart gets its OWN list -- not a shared one.
    items: list[str] = Field(default_factory=list)
    # Same rule for dicts: metadata per-instance.
    metadata: dict[str, str] = Field(default_factory=dict)


a = Cart()
b = Cart()
a.items.append("book")            # mutating a should not affect b
print("a.items:", a.items)        # ['book']
print("b.items:", b.items)        # []  -- independent list
print("same object?", a.items is b.items)  # False


# Contrast: writing `items: list[str] = []` would silently share ONE list
# between every Cart ever created. Pydantic v2 actually blocks this for you,
# but default_factory is the idiomatic fix everywhere.


# Factories can be any zero-arg callable, including a lambda for a constant
# structure that still needs to be copied per instance.
class Config(BaseModel):
    flags: dict[str, bool] = Field(default_factory=lambda: {"debug": False})


print(Config().flags)             # {'debug': False}
