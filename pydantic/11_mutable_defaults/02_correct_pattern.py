"""
Correct pattern: default_factory
================================
`Field(default_factory=...)` gives every instance its OWN fresh mutable.

Cheat sheet
---------------------------------------------------------------------------
Field(default_factory=list)                      fresh empty list per instance
Field(default_factory=dict)                      fresh empty dict per instance
Field(default_factory=set)                       fresh empty set per instance
Field(default_factory=lambda: {"v": 1})          copied literal (safe to mutate)
Field(default_factory=uuid.uuid4)                unique id per row
Field(default_factory=lambda: datetime.now(tz))  fresh UTC timestamp

⚠️ Gotchas
- Factory must be a ZERO-ARG callable. `list` works; `list("abc")` does not.
- `= []` evaluates once at class-load -- avoid even though Pydantic copies it.
- `datetime.utcnow` is deprecated in 3.12+; use `datetime.now(timezone.utc)`.
"""

from pydantic import BaseModel, Field


class Cart(BaseModel):
    # Factory runs fresh on EVERY new Cart -- no accidental cross-instance sharing.
    items: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)
    tags: set[str] = Field(default_factory=set)


a, b = Cart(), Cart()
a.items.append("apple")
a.metadata["coupon"] = "SPRING10"

print(a.model_dump())  # items=['apple'], metadata has coupon
print(b.model_dump())  # items=[], metadata={} -- fully independent
