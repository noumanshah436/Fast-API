# 22. ORM Mode — `from_attributes`

## ⚡ TL;DR
Let Pydantic read fields via `getattr(obj, name)` instead of `obj["name"]` —
so SQLAlchemy rows (or any attribute-bearing object) validate directly.

## 🎯 When to use
- Converting SQLAlchemy rows into FastAPI response models
- Any source that exposes data as attributes, not a mapping
- Bridging persistence objects to wire DTOs without manual copying

## v1 → v2 rename
| v1 | v2 |
|----|----|
| `class Config: orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `Model.from_orm(row)` | `Model.model_validate(row)` |

## Key points
- Opt-in flag: `ConfigDict(from_attributes=True)`
- `model_validate(obj)` walks attrs by field name
- Nested relationships (e.g. `order.items`) resolve recursively
- Schema is a **security boundary** — fields absent from the DTO never leak

## ⚠️ Gotchas
- Forgetting the flag -> `ValidationError: input should be a valid dictionary`
- Lazy-loaded SQLAlchemy relationships trigger queries during validation
- `EmailStr` requires `pip install email-validator`

## Files
| File | Purpose |
|------|---------|
| `01_from_attributes.py` | Minimum example with a fake ORM object |
| `02_sqlalchemy_example.py` | FastAPI `response_model` pattern |
