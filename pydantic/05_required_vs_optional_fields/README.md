# 5. Required vs Optional Fields

> ⚡ **TL;DR** — A field is required **iff it has no default**. Type hints (`Optional`, `X | None`) describe allowed *values*, not whether the caller may omit the field.

## 🎯 The truth table

| Declaration | Required? | Accepts `None`? |
|---|---|---|
| `name: str` | ✅ | ❌ |
| `name: str = "Anon"` | ❌ | ❌ |
| `name: str \| None` | ✅ | ✅ |
| `name: str \| None = None` | ❌ | ✅ |
| `name: str = Field(..., min_length=1)` | ✅ | ❌ |

## ⚡ The #1 gotcha

```python
class Profile(BaseModel):
    nickname: Optional[str]   # REQUIRED — must pass, even as None
```

`Optional[X]` == `X | None`. It says *"value may be None"*, **not** *"caller may omit"*. Presence is controlled by defaults alone.

## 🎯 Making "required" explicit

- `name: str` — implicit (no default)
- `name: str = Field(..., min_length=1)` — `...` (Ellipsis) = "no default" + lets you attach constraints / description

## ⚠️ Gotchas

- Defaults are **validated** too — a bad default raises as early as first use (or at class definition with `validate_default=True`).
- Mutable defaults: use `Field(default_factory=list)`, not `= []` on plain types. (Pydantic actually handles `= []` safely by deep-copying, but the factory form is the idiomatic, universal fix.)
- `x: str = None` "works" but the type hint lies — prefer `x: str | None = None`.

## Files

| File | Description |
|---|---|
| `01_required_fields.py` | No-default, `Field(...)`, `missing` vs constraint errors |
| `02_optional_fields.py` | `Optional[X]` ≠ "may omit" — the classic trap |
| `03_default_values.py` | Static defaults, `default_factory`, validated defaults |
