# 23. Model Inheritance

Pydantic models inherit like normal classes: fields and validators propagate.
This is how you split one "domain entity" into Create / Read / Update schemas
without duplication.

## Key takeaways

- Subclasses inherit fields, validators, and config.
- Override a field by redeclaring it — same name, new type/constraints.
- Common pattern: one `Base*` with shared fields, siblings per use case.

## When to use

- FastAPI request/response schemas for the same resource.
- Splitting "internal" vs "public" views of a model.
- Partial-update (PATCH) schemas where every field is optional.

## Files

| File | Purpose |
|------|---------|
| `01_basic_inheritance.py` | Create / Update / Response trio from one base. |
| `02_extending_fields.py` | Override field type or constraints in a subclass. |
