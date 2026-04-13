# 10 - Model Config

**⚡ TL;DR** — `model_config = ConfigDict(...)` is the single knob-panel for a
model's behavior. ConfigDict is typed, so flag names are autocompleted.

## 🎯 When to reach for it

| Situation                                        | Flag                          |
|--------------------------------------------------|-------------------------------|
| Unknown keys must fail loudly (API inputs)       | `extra="forbid"`              |
| Build from SQLAlchemy / dataclass / any object   | `from_attributes=True`        |
| Accept both `camelCase` and `snake_case` on input| `populate_by_name=True`       |
| Catch bad writes after construction              | `validate_assignment=True`    |
| Immutable value object (hashable, dict-key-able) | `frozen=True`                 |
| Auto-trim whitespace on all `str` fields         | `str_strip_whitespace=True`   |

## Extra-fields policies

| Value       | Behavior                        | Best for                |
|-------------|---------------------------------|-------------------------|
| `"ignore"`  | drop unknown keys silently (default) | lenient readers     |
| `"forbid"`  | raise `extra_forbidden`         | strict API contracts    |
| `"allow"`   | keep as attributes, show in dump| webhook envelopes       |

## ⚠️ Gotchas

- v1's inner `class Config:` is **gone** — use `model_config = ConfigDict(...)`.
- v1 `orm_mode=True` → v2 `from_attributes=True` (same feature, better name).
- `extra="ignore"` is the default — typos in client payloads vanish silently.
- `frozen=True` is class-wide and blocks **all** attribute writes.
- `validate_assignment=True` re-runs validators on every set — slight cost per write.

## Files

| File | Shows |
|------|-------|
| `01_model_config_basics.py` | `ConfigDict`, `validate_assignment`, `str_strip_whitespace` |
| `02_extra_fields.py`        | `ignore` vs `forbid` vs `allow`                            |
| `03_from_attributes.py`     | building models from ORM rows / arbitrary objects          |
