"""
Optional Fields -- the common pitfall
=====================================
`Optional[X]` means "X or None", NOT "may be omitted". Defaults decide that.
"""

from typing import Optional

from pydantic import BaseModel, ValidationError


class Profile(BaseModel):
    # Required -- the value may be None, but you MUST pass it explicitly.
    # This catches the "did the caller forget, or intentionally clear?" case.
    nickname: Optional[str]

    # Not required -- omitted calls default to None.
    # Use this for truly optional fields in request bodies.
    bio: Optional[str] = None

    # Modern Python 3.10+ style -- same meaning as Optional[str] = None.
    avatar_url: str | None = None


# Must pass nickname, even as None.
p = Profile(nickname=None)
print(p)  # nickname=None bio=None avatar_url=None


# Forgetting nickname -> "missing", even though its type allows None.
# This is the #1 Pydantic gotcha. `Optional` is about type, not presence.
try:
    Profile()
except ValidationError as e:
    print(e.errors()[0]["type"], e.errors()[0]["loc"])   # missing ('nickname',)


# Passing all three works as expected.
full = Profile(nickname="al", bio="hi", avatar_url="https://x/y.png")
print(full.model_dump())
