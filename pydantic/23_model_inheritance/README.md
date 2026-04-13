# 23. Model Inheritance

## ⚡ TL;DR
Pydantic models inherit like normal classes — fields, validators, and config
all propagate. This is how you split one entity into Create / Read / Update
schemas without duplication.

## 🎯 When to use
- FastAPI request/response schemas for the same resource
- Separating internal vs public views of a model
- PATCH schemas where every field must be optional
- Specialising a base schema with stricter constraints

## Key points
- Subclasses inherit fields, validators, and `model_config`
- Override a field by redeclaring it (same name, new type / constraints)
- Overrides **replace** the Field — repeat constraints you still need
- Validators inherit unless shadowed in the child

## Common pattern
```
UserBase        shared fields
├── UserCreate  + password (write-only)
├── UserUpdate  all Optional (PATCH) — usually does NOT inherit Base
└── UserRead    + id, created_at; from_attributes=True
```

## ⚠️ Gotchas
- v2 does not auto-default `Optional[X]` to `None` — write `= None` yourself
- Don't inherit `Base` for PATCH schemas — inherited required fields stay required
- No built-in way to "remove" an inherited field — use a sibling model instead

## Files
| File | Purpose |
|------|---------|
| `01_basic_inheritance.py` | Create / Update / Response trio from one base |
| `02_extending_fields.py` | Override field type or constraints in a subclass |
