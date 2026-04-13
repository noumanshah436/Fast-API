# 07 - Aliases and Field

`Field()` is how you attach metadata and constraints to a field beyond its type.
Aliases let you decouple the Python attribute name from the wire format (JSON).

## Key takeaways

- `Field()` adds description, title, examples, and constraints that flow into JSON schema.
- `alias="camelName"` maps external (JSON) keys to Python snake_case attributes.
- Set `model_config = ConfigDict(populate_by_name=True)` to accept either name.
- Constraints (`gt`, `ge`, `lt`, `le`, `min_length`, `max_length`, `pattern`) run during validation.

## When / why

- Building FastAPI endpoints where the client sends camelCase JSON but your code uses snake_case.
- Generating OpenAPI docs that need rich field descriptions and examples.
- Enforcing business rules (age > 0, password length >= 8) at the model boundary.

## Files

| File | What it shows |
|------|---------------|
| `01_field_basics.py` | `Field()` with description/title/default, JSON schema output |
| `02_field_aliases.py` | camelCase aliases, `populate_by_name` |
| `03_field_constraints.py` | numeric and string constraints, regex patterns |
