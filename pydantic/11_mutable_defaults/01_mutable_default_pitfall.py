"""
Mutable default pitfall
=======================
One list reused across instances -- the classic Python footgun.
"""

from pydantic import BaseModel


# --- The bug in a plain class ---------------------------------------------
class BadCart:
    items: list = []  # class attribute, ONE list object shared everywhere


a = BadCart()
b = BadCart()
a.items.append("apple")
print("shared?", b.items)  # ['apple'] -- b got a's data. Ugh.


# --- Dataclasses refuse to let you do this --------------------------------
# from dataclasses import dataclass
# @dataclass
# class BadCartDC:
#     items: list = []   # -> ValueError at class definition time
# You MUST use: items: list = field(default_factory=list)


# --- Pydantic deep-copies defaults per instance ---------------------------
class PydanticCart(BaseModel):
    items: list = []  # works, but still bad style -- prefer default_factory


x = PydanticCart()
y = PydanticCart()
x.items.append("apple")
print("pydantic isolated?", y.items)  # [] -- Pydantic protected us

# WHY the bug exists in plain Python: default values are evaluated ONCE, at
# class-definition time. Every instance that doesn't explicitly set the field
# sees the same object. Pydantic copies defaults during validation; plain
# Python and dataclasses (without field()) do not.
