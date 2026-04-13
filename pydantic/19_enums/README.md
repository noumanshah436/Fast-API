# Enums

Pydantic validates Python `Enum` members and accepts either the enum
instance or its raw value as input.

## Key takeaways
- Subclass `str, Enum` so the value is JSON-serializable directly.
- By default `model_dump()` yields the enum *instance*; JSON dump yields the value.
- `model_config = ConfigDict(use_enum_values=True)` dumps the raw value everywhere.
- Invalid values raise a `ValidationError` listing all allowed members.

## When / why
- Fixed vocabularies: roles, statuses, currency codes, environments.
- Replaces stringly-typed fields with autocompletion and safe refactors.
- Cleaner JSON schema: enums render as `"enum": [...]` in OpenAPI.

## Files
| File | Topic |
|------|-------|
| 01_enum_field.py | Declaring an enum field, accepted inputs |
| 02_enum_use_enum_values.py | `use_enum_values=True` for raw-value dumps |
