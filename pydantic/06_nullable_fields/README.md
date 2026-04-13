# Topic 6: Nullable Fields

**⚡ TL;DR** — `| None` widens the *type*. A *default* makes the field omittable.
Two independent axes — mix them to match your API contract.

## The 2x2

| Declaration             | Accepts None? | Can omit? | Typical use           |
|-------------------------|---------------|-----------|-----------------------|
| `x: str`                | no            | no        | required + non-null   |
| `x: str = "x"`          | no            | yes       | safe default          |
| `x: str \| None`        | yes           | no        | PATCH / required-null |
| `x: str \| None = None` | yes           | yes       | truly optional        |

## 🎯 When to use

- **Mirror a NULLABLE DB column in a write model** → `str | None = None`
- **PATCH body** (omit ≠ null) → `str | None` + `model_dump(exclude_unset=True)`
- **Config loader / trailing metadata** → `str | None = None`

## ⚠️ Gotchas

- `Optional[X]` in v2 does NOT imply `= None`. Add the default yourself.
- Passing `None` to a non-nullable field → `*_type` error (e.g. `string_type`).
- `exclude_unset` (never set) ≠ `exclude_none` (set to None). PATCH needs `exclude_unset`.

## Files

| File | Shows |
|------|-------|
| `01_allowing_none.py` | `str \| None` — nullable type, still required |
| `02_optional_vs_nullable.py` | PATCH vs PUT: the omit/null distinction |
