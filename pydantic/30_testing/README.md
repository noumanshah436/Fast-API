# 30. Testing Pydantic Models

## ⚡ TL;DR
Pydantic models are deterministic: valid input constructs, invalid input raises `ValidationError`. Pin both paths with pytest, assert on structured `type` / `loc` (not message text), and use a factory to keep tests focused.

## 🎯 When to use
- Locking in business-rule validators against regressions.
- Catching breaking schema changes before they hit production.
- Keeping tests readable as models grow to 20+ fields.

## 🔁 Cheat sheet

| Path            | Pattern                                                          |
|-----------------|------------------------------------------------------------------|
| Happy path      | `assert Model(**valid).field == expected`                        |
| Sad path        | `with pytest.raises(ValidationError) as exc_info:`               |
| Missing field   | `errors[0]["type"] == "missing"` and `loc == ("email",)`         |
| Wrong type      | `errors[0]["type"] == "int_parsing"` (and friends)               |
| Many fields     | `make_user(**overrides)` factory — override only what you test   |

## ⚠️ Gotchas
- Don't assert on `err["msg"]` — human text is NOT stable API. Assert on `type` + `loc`.
- `loc` is a tuple, not a string — `("address", "zip")` for nested errors.
- `ValidationError` groups multiple failures; `len(errors)` matters when you expect exactly one.
- A factory with `{**defaults, **overrides}` is cheaper than pytest fixtures for simple cases and reads better inline.

## Files

| File | Purpose |
|------|---------|
| `01_testing_validation.py` | Happy and sad path basics with pytest. |
| `02_testing_error_details.py` | Assert on `type` and `loc`, not messages. |
| `03_factory_pattern.py` | `make_user(**overrides)` for clean fixtures. |
