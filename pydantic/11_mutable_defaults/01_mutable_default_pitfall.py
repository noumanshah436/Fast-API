"""
Mutable default pitfall
=======================
The shared-list footgun: what plain Python, @dataclass, and Pydantic each do.

Behavior across frameworks
---------------------------------------------------------------------------
Plain class   `items: list = []`             → ONE shared list, silent bleed
@dataclass    `items: list = []`             → ValueError at class-definition
Pydantic v2   `items: list = []`             → deep-copied per instance (ok)
Idiomatic     `Field(default_factory=list)`  → ALWAYS correct, portable

Why the bug exists
- Class-level defaults are evaluated ONCE, when the class body runs.
- Every instance that omits the value binds to that SAME object.
- Pydantic hides this by copying defaults during validation; plain Python
  and dataclasses give you no such safety net.

Rule of thumb: write `default_factory` even when Pydantic would save you --
intent is explicit and the pattern survives a port to dataclass / plain class.
"""

from pydantic import BaseModel


# Plain class -- the classic footgun.
class BadCart:
    items: list = []  # class attribute: ONE list shared across ALL instances


a, b = BadCart(), BadCart()
a.items.append("apple")
print("shared?", b.items)  # ['apple'] -- b sees a's mutation

# @dataclass refuses this at class-definition time:
#   @dataclass class X: items: list = []     -> ValueError
#   must use:  items: list = field(default_factory=list)


# Pydantic silently deep-copies defaults -- works, but still poor style.
class PydanticCart(BaseModel):
    items: list = []


x, y = PydanticCart(), PydanticCart()
x.items.append("apple")
print("pydantic isolated?", y.items)  # [] -- Pydantic copied the default
