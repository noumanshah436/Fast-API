# 09 - Field Defaults

**⚡ TL;DR** — `x: int = 0` and `x: int = Field(default=0)` mean the same thing.
Reach for `Field()` when you also want metadata, constraints, or a factory.

## Forms at a glance

| Form                                              | Required? | Use when                                   |
|---------------------------------------------------|-----------|--------------------------------------------|
| `x: int`                                          | yes       | simple required field, no metadata         |
| `x: int = Field(...)`                             | yes       | required + constraints/description         |
| `x: int = 0`                                      | no        | simple default                             |
| `x: int = Field(default=0, description="...")`    | no        | default + metadata                         |
| `x: list[int] = Field(default_factory=list)`      | no        | mutable default (must be a factory!)       |

## 🎯 When / why

- Need description/alias **with** a default → `Field(default=..., ...)`.
- Required **with** constraints (e.g. `min_length=3`) → `Field(..., min_length=3)`.
- Mutable or time-based default → **always** `default_factory`, never a literal.

## ⚠️ Gotchas

- Never write `x: list[int] = []` — use `default_factory=list`. Same for dicts/sets.
- Use `datetime.now(timezone.utc)` inside a factory, not `datetime.utcnow()` (deprecated).
- `Field(...)` (ellipsis) and no-assignment are both "required" — prefer `Field(...)`
  when constraints are attached so intent is obvious at the call site.

## Files

| File | Shows |
|------|-------|
| `01_default_values.py`      | literal defaults, `Field(default=...)`, `default_factory` |
| `02_ellipsis_required.py`   | `Field(...)` — required fields that carry constraints     |
