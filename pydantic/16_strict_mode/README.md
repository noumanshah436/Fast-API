# 16. Strict Mode

By default Pydantic is **lax**: `"42"` becomes `42`, `"true"` becomes `True`.
Great for HTTP query strings and form data -- dangerous when you need exact
types (money, auth tokens, IDs from trusted internal services).

## Key Takeaways
- Default mode coerces compatible types -- a feature, not a bug.
- `StrictInt`, `StrictStr`, `StrictBool`, `StrictFloat` reject cross-type input.
- `model_config = ConfigDict(strict=True)` turns strict mode on for the whole
  model -- every field must match its declared type exactly.
- Per-call strictness: `Model.model_validate(data, strict=True)`.

## When to Use It
- Financial / accounting code (no silent `"10"` -> `10`).
- Auth APIs where `"false"` accidentally becoming `True` is a vuln.
- Internal service-to-service contracts where both sides already speak JSON
  with real types.

## Files
- `01_type_coercion.py` -- the default lax behavior and its mental model.
- `02_strict_types.py` -- StrictX fields and model-wide strict config.
