# 29. Error Customization

## ⚡ TL;DR
Pydantic's default errors are structured but terse. Raise `ValueError` inside a validator to inject your own message, then flatten `e.errors()` into the `{field: message}` shape frontends expect.

## 🎯 When to use
- Public-facing APIs where "value is not a valid..." is too technical.
- Frontend forms that consume a map of `field -> error string`.
- Teams that want one consistent 422 body across every endpoint.

## 🔁 Cheat sheet

| Want                                | Do this                                               |
|-------------------------------------|-------------------------------------------------------|
| Custom message on a field           | `raise ValueError("...")` inside `@field_validator`   |
| Access structured error list        | `e.errors()` → list of `{loc, msg, type, input, ctx}` |
| Flat `{field: message}` for JSON    | Join `loc` with `.`, strip `"Value error, "` prefix   |
| Cross-field rule                    | `@model_validator(mode="after")` + `raise ValueError` |

## ⚠️ Gotchas
- Pydantic prefixes `ValueError` text with `"Value error, "` in `err["msg"]`. Strip it, or read `err["ctx"]["error"]`.
- `loc` is a tuple (e.g. `("address", "zip")`) — join it before putting in a JSON body.
- Don't assert on exact message strings in tests — they drift. Assert on `type` (e.g. `"value_error"`, `"missing"`).
- Keep messages actionable — tell the user what to fix, not the internal rule name.

## Files

| File | Purpose |
|------|---------|
| `01_custom_messages.py` | Raise `ValueError` inside `@field_validator` for readable messages. |
| `02_user_friendly_errors.py` | Collapse `errors()` into a flat `{field: message}` dict. |
