# Private Attributes

Per-instance state that is **not** a validated field: not in the input,
not in `model_dump()`, not in the JSON schema.

## Key takeaways
- Use `PrivateAttr()` (optionally with `default` / `default_factory`).
- Alternatively, name a field with a leading underscore (`_cache`).
- Private attrs are skipped by validation and serialization entirely.
- Initialize them in `model_post_init` when you need access to field values.

## When / why
- Caches, memoized computations, lazy clients (DB, HTTP).
- Counters, timestamps, internal flags the API must not expose.
- Anything that must not round-trip through JSON.

## Files
| File | Topic |
|------|-------|
| 01_private_attr.py | `PrivateAttr()` for internal state |
| 02_underscore_fields.py | Leading-underscore names and initialization |
