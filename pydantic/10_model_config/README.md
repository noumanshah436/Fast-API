# 10 - Model Config

`model_config` is how you tune a model's behavior: strictness, extra fields,
ORM support, validation on assignment, and more.

## Key takeaways

- In Pydantic v2, config lives in a class-level `model_config = ConfigDict(...)`.
- Pydantic v1 used an inner `class Config:` block -- that's gone.
- `extra="ignore"` (default), `"forbid"`, or `"allow"` controls unknown fields.
- `from_attributes=True` lets a model be built from any object's attributes --
  classic SQLAlchemy / ORM use case.
- Other useful flags: `validate_assignment`, `str_strip_whitespace`, `frozen`.

## When / why

- `extra="forbid"` for request payloads where unknown keys indicate client bugs.
- `from_attributes=True` to convert a SQLAlchemy row into a response model.
- `populate_by_name=True` alongside aliases for flexible input parsing.

## Files

| File | What it shows |
|------|---------------|
| `01_model_config_basics.py` | `ConfigDict` vs legacy inner `class Config` |
| `02_extra_fields.py` | `ignore` vs `forbid` vs `allow` comparison |
| `03_from_attributes.py` | Building models from ORM-like objects |
