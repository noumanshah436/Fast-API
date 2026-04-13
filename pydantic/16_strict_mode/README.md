# 16. Strict Mode

## ⚡ TL;DR
Pydantic is **lax by default** -- `"42"` becomes `42`, `"true"` becomes `True`. Strict mode disables that, per-field, per-model, or per-call.

## 🎯 When to use
- Money / accounting -- no silent `"10"` -> `10`.
- Auth APIs -- a stray `"false"` becoming `True` is a vulnerability.
- Internal service-to-service JSON -- both ends already speak real types.
- Leave public HTTP / form endpoints on default lax.

## 🔧 Three scopes

| Scope | API | Use when |
|------|-----|----------|
| Per field | `StrictInt`, `StrictStr`, `StrictBool`, `StrictFloat` | Only a few sensitive fields |
| Per model | `model_config = ConfigDict(strict=True)` | Whole model is internal |
| Per call  | `Model.model_validate(data, strict=True)` | One trusted boundary |

## ⚠️ Gotchas
- In lax mode, whole-number floats (`3.0`) pass as `int`; `3.5` fails (lossy).
- `bool` is the widest coercer -- `"1"`, `"yes"`, `"on"` all pass.
- `StrictBool` rejects `0` and `1` -- only real `True`/`False` pass.

## Files
| File | Topic |
|------|-------|
| 01_type_coercion.py | Default lax behaviour + mental model |
| 02_strict_types.py  | `StrictX` fields + `ConfigDict(strict=True)` |
