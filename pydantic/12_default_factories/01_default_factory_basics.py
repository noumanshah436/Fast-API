"""
default_factory basics
======================
One fresh mutable per instance -- the end of shared-list bugs.

Cheat sheet
---------------------------------------------------------------------------
Field(default_factory=list)                empty list
Field(default_factory=dict)                empty dict
Field(default_factory=set)                 empty set
Field(default_factory=lambda: {"k": 0})    copied literal (safe to mutate)

Rules
- Factory is any zero-arg callable; Pydantic calls it per new instance.
- Wrap arguments in a lambda: `default_factory=lambda: Counter({"a": 1})`.
- Stricter configs actively reject `= []`; the factory is idiomatic anyway.
"""

from pydantic import BaseModel, Field


class Cart(BaseModel):
    items: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


a, b = Cart(), Cart()
a.items.append("book")
print(a.items, b.items)           # ['book'] []
print(a.items is b.items)         # False -- different objects


# Lambda wraps a literal dict so each Config gets its own copy.
class Config(BaseModel):
    flags: dict[str, bool] = Field(default_factory=lambda: {"debug": False})


print(Config().flags)             # {'debug': False}
