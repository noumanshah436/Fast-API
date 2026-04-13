"""
Default Values
==============
Any field with a default is non-required — and defaults are validated too.

Three ways to default
---------------------
host: str = "0.0.0.0"                       →  static literal
origins: list[str] = Field(default_factory=list)  →  fresh mutable per instance
created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

Mutable defaults
----------------
Pydantic deep-copies `= []` safely (unlike stdlib dataclasses) — but
`default_factory=list` is the idiomatic, universal form and is required
when the factory has side effects (e.g., datetime.now).

Defaults are validated
----------------------
- Constraints still apply when the caller OVERRIDES a default.
- Set `validate_default=True` on the field to validate the literal default itself.
"""

from pydantic import BaseModel, Field, ValidationError


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Fresh list per instance — no shared-mutable-state bug.
    allowed_origins: list[str] = Field(default_factory=list)

    # Default is used when omitted, but overrides still hit the constraint.
    max_connections: int = Field(default=100, ge=1, le=1000)


# Omit everything — all defaults apply.
cfg = AppConfig()
print(cfg)

# Override any subset.
cfg2 = AppConfig(port=9000, debug=True, allowed_origins=["https://app.com"])
print(cfg2.model_dump())


# Overrides still pass through validation — defaults don't grant a bypass.
try:
    AppConfig(max_connections=5000)
except ValidationError as e:
    print(e.errors()[0]["type"])   # less_than_equal


# Proof: instances don't share the default list.
a, b = AppConfig(), AppConfig()
a.allowed_origins.append("x")
print(a.allowed_origins, b.allowed_origins)   # ['x'] []
