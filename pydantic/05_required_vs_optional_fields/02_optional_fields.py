"""
Optional Fields — the #1 Pydantic trap
======================================
`Optional[X]` means "X or None". It does NOT mean "the caller may omit it".

Required vs presence — decoupled
--------------------------------
Declaration                        Required?   Accepts None?
-----------------------------------------------------------------
x: str                             yes         no
x: Optional[str]   (== str|None)   yes         yes   ← the trap
x: Optional[str] = None            no          yes
x: str | None = None               no          yes   (modern 3.10+ form)

Rule of thumb
-------------
- Want "caller may omit"?   → add `= None` (or any default)
- Want "value can be None"? → add `| None` to the type
- Want both?                → both, together
"""

from typing import Optional

from pydantic import BaseModel, ValidationError


class Profile(BaseModel):
    # Required — value may be None, but caller MUST pass it.
    # Useful when you need to distinguish "forgot" from "explicit null".
    nickname: Optional[str]

    # Not required — defaults to None if omitted.
    bio: Optional[str] = None

    # Modern syntax — identical meaning to `Optional[str] = None`.
    avatar_url: str | None = None


# Works: nickname passed explicitly as None.
p = Profile(nickname=None)
print(p)


# Omitting nickname → "missing", even though None is in its type.
# This is the trap: `Optional` is about the type, not about presence.
try:
    Profile()
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])   # missing ('nickname',)


full = Profile(nickname="al", bio="hi", avatar_url="https://x/y.png")
print(full.model_dump())
