"""
Legacy constrained helpers
==========================
`constr`, `conint`, `confloat` still work in v2 -- but they're legacy.

Legacy                          Modern (v2)
-----------------------------------------------------------------
constr(min_length=3)            Annotated[str, Field(min_length=3)]
conint(ge=0, lt=130)            Annotated[int, Field(ge=0, lt=130)]
confloat(ge=0.0, le=1.0)        Annotated[float, Field(ge=0, le=1)]

Why Annotated + Field wins:
- One consistent shape across str / int / float / list / etc.
- Composes cleanly with custom validators: Annotated[..., AfterValidator(fn)]
- Base type remains visible to IDEs and mypy.
- `con*` returns a dynamic type -- worse static inference.
"""

from pydantic import BaseModel, confloat, conint, constr


class LegacyUser(BaseModel):
    # Works, but reads worse in hints and is harder to compose with validators.
    username: constr(min_length=3, max_length=20, pattern=r"^[a-z]+$")
    age: conint(ge=0, lt=130)
    score: confloat(ge=0.0, le=1.0)


print(LegacyUser(username="alice", age=30, score=0.8))
