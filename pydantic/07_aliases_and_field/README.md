# 07 - Aliases and `Field()`

**⚡ TL;DR** — `Field()` decorates a field with metadata, constraints, and aliases.
Aliases decouple your Python attribute names from the wire JSON.

## 🎯 When to reach for it

| Situation | Use |
|-----------|-----|
| Frontend sends `camelCase`, backend is `snake_case` | `alias="fooBar"` + `populate_by_name=True` |
| Need a description in `/docs` | `Field(..., description="...")` |
| Required field with constraints | `Field(..., min_length=3)` |
| Optional with constraint | `Field(default=None, ge=0)` |

## Constraints cheatsheet

| Kind    | Args                                         |
|---------|----------------------------------------------|
| Numeric | `gt`, `ge`, `lt`, `le`, `multiple_of`        |
| String  | `min_length`, `max_length`, `pattern`        |
| Seq     | `min_length`, `max_length`                   |

## ⚠️ Gotchas

- Without `populate_by_name=True`, constructing by the Python name raises.
- `alias` governs both in and out; use `validation_alias` / `serialization_alias` to split.
- `Field(...)` (ellipsis) = explicit "required".

## Files

| File | Shows |
|------|-------|
| `01_field_basics.py` | metadata → JSON schema |
| `02_field_aliases.py` | camelCase ↔ snake_case, `populate_by_name` |
| `03_field_constraints.py` | numeric / string / regex bounds |
