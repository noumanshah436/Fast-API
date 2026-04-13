# Computed Fields

Read-only values derived from other fields that should appear in the
serialized output and JSON schema.

## Key takeaways
- Decorate a `@property` with `@computed_field` to include it in `model_dump()`.
- A plain `@property` stays on the instance but is **not** serialized.
- Computed fields are read-only -- no assignment, no input validation.
- They show up in the generated JSON schema, so API consumers see them.

## When / why
- `full_name` from `first_name + last_name`.
- `total` from `price * quantity` for an invoice line.
- Any derived value clients should see but should never send.

## Files
| File | Topic |
|------|-------|
| 01_computed_field.py | `@computed_field` in action |
| 02_when_to_use.py | `@computed_field` vs plain `@property` |
