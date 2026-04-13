"""
Default Values
==============
Any field with a default is non-required -- and the default is validated too.
"""

from pydantic import BaseModel, Field, ValidationError


class AppConfig(BaseModel):
    # Simple defaults -- used verbatim when the key is absent.
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Mutable default via Field(default_factory=...) -- each instance gets
    # its own list. Avoids the classic "shared mutable default" bug.
    allowed_origins: list[str] = Field(default_factory=list)

    # Defaults ARE validated on model creation by default. A bad default
    # won't silently slip through -- it raises at class definition time if
    # you set validate_default=True, or on first use otherwise.
    max_connections: int = Field(default=100, ge=1, le=1000)


# No args needed -- all defaults apply.
cfg = AppConfig()
print(cfg)

# Override any subset; the rest stay as defaults.
cfg2 = AppConfig(port=9000, debug=True, allowed_origins=["https://app.com"])
print(cfg2.model_dump())


# Explicit override still runs validation -- you cannot bypass constraints
# just because a field has a default.
try:
    AppConfig(max_connections=5000)
except ValidationError as e:
    print(e.errors()[0]["type"])   # less_than_equal


# Each instance has its own list -- no cross-contamination.
a, b = AppConfig(), AppConfig()
a.allowed_origins.append("x")
print(a.allowed_origins, b.allowed_origins)   # ['x'] []
