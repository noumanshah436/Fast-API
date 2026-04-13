# 13. Custom Serializers

`@field_serializer` lets you control exactly how a field is emitted by
`model_dump()` / `model_dump_json()` -- handy for dates, decimals, enums, and
any type whose default representation does not match your API contract.

## Key Takeaways
- Decorate a method with `@field_serializer("field_name")` to override output.
- Runs only on serialization (`model_dump`), not on input validation.
- Use `when_used="json"` to only customize JSON output (keep Python dict raw).
- For enums: default JSON output is the **value**; use a serializer to emit
  the name, or to coerce to `str` / `int` explicitly.

## When to Use It
- Formatting `datetime` as a specific ISO string or epoch int.
- Rendering `Decimal` as `str` so clients do not lose precision.
- Hiding or masking sensitive fields (`****1234`).
- Emitting enum `.name` instead of `.value` for human-readable APIs.

## Files
- `01_field_serializer.py` -- datetime + Decimal formatting.
- `02_serializing_enums.py` -- value vs name output.
