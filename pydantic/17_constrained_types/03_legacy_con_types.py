"""
Legacy constrained helpers: constr, conint, confloat
====================================================
Still available in v2 but Annotated + Field is the preferred style.
"""

from pydantic import BaseModel, constr, conint, confloat


class LegacyUser(BaseModel):
    # These factory functions build a type with constraints baked in.
    # Works fine -- but harder to compose with other Annotated metadata.
    username: constr(min_length=3, max_length=20, pattern=r"^[a-z]+$")
    age: conint(ge=0, lt=130)
    score: confloat(ge=0.0, le=1.0)


print(LegacyUser(username="alice", age=30, score=0.8))

# Why prefer Annotated + Field instead:
# - One consistent pattern across str, int, float, list, etc.
# - Plays nicely with custom validators via Annotated[..., AfterValidator(fn)].
# - Better IDE / type-checker support -- the base type stays visible.
