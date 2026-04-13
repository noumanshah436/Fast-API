# 29. Error Customization

Pydantic's default errors are structured but terse. For public APIs you
usually want **custom messages** and a **shape the frontend can consume**
(like `{"field": "message"}`).

## Key Takeaways
- `@field_validator` raising `ValueError("...")` surfaces your message in `ValidationError`.
- `e.errors()` returns a list of dicts with `loc`, `msg`, `type`, `input`.
- Convert that list to a flat `{field: message}` dict for JSON responses.
- Keep business-facing messages in the validator; keep the HTTP shaping in one helper.

## When / Why
- You want "Username must be lowercase" instead of "value is not a valid...".
- Frontend forms expect a map of field -> error string.
- You need consistent error payloads across many endpoints.

## Files
- `01_custom_messages.py` -- raise `ValueError` inside a validator.
- `02_user_friendly_errors.py` -- `errors()` list -> flat dict helper.
