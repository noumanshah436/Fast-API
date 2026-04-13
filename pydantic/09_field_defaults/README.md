# 09 - Field Defaults

Two equivalent ways to declare a default, plus the explicit "required" marker.

## Key takeaways

- `x: int = 0` and `x: int = Field(default=0)` are equivalent -- the second just
  lets you attach metadata (description, alias) alongside.
- `Field(...)` (ellipsis) means "required" -- use it when you need constraints
  but no default.
- A field with no default and no `...` is also required, but using `Field(...)`
  keeps intent obvious when metadata is present.

## When / why

- Reach for `Field(default=...)` once you need a description, alias, or
  constraints together with a default value.
- Use `Field(...)` when a field is required AND needs constraints like
  `min_length` -- you can't just write `name: str = min_length=3`.

## Files

| File | What it shows |
|------|---------------|
| `01_default_values.py` | direct assignment vs `Field(default=...)` |
| `02_ellipsis_required.py` | `Field(...)` for required fields with constraints |
