# 17. Constrained Types

## ⚡ TL;DR
Push invariants into the type itself: length, range, regex, step. The v2-native shape is `Annotated[T, Field(...)]` -- legacy `constr` / `conint` / `confloat` still work but compose poorly with validators.

## 🎯 When to use
- Reject bad input at the edge (usernames, prices, quantities).
- Replace scattered `if` checks with a single declarative rule.
- Auto-document constraints in the generated JSON / OpenAPI schema.

## 🔧 Cheatsheet

| Target | Constraint kwargs |
|--------|------------------|
| `str`  | `min_length`, `max_length`, `pattern`, `strip_whitespace`, `to_lower`, `to_upper` |
| `int` / `float` | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan` |
| `list` / `set` / `dict` | `min_length`, `max_length` |
| `Decimal` | `max_digits`, `decimal_places` |

## ⚠️ Gotchas
- `pattern` must match the whole string in v2 (not `re.search`-style).
- `strip_whitespace` runs before length checks -- `"   "` can violate `min_length=1`.
- `bool` is a subclass of `int` -- `gt=0` still accepts `True` unless strict is on.
- Reassignment re-validates only with `ConfigDict(validate_assignment=True)`.

## Files
| File | Topic |
|------|-------|
| 01_field_constraints.py | String constraints via `Annotated + Field` |
| 02_numeric_constraints.py | Numeric bounds and `multiple_of` |
| 03_legacy_con_types.py | Legacy `constr` / `conint` / `confloat` |
