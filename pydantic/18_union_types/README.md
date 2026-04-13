# Union Types

A field that accepts more than one type. Pydantic v2 uses *smart mode* by
default -- it picks the best-matching member instead of blindly trying
left-to-right.

## Key takeaways
- `int | str` (PEP 604) is the v2-native way to declare unions.
- Smart mode picks the exact-type match when possible; no data coercion surprises.
- For polymorphic payloads, use **discriminated (tagged) unions** -- faster,
  clearer errors, and cleaner JSON schema.

## When / why
- Webhook payloads with different shapes keyed by a `type` field.
- API endpoints that accept multiple input formats (id number or slug string).
- Event sourcing / command buses where a single channel carries many shapes.

## Files
| File | Topic |
|------|-------|
| 01_union_basics.py | `X \| Y` unions and smart validation |
| 02_discriminated_union.py | `Field(discriminator=...)` for tagged payloads |
