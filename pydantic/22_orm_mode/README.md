# 22. ORM Mode (`from_attributes`)

Pydantic normally reads data from a `dict`. ORM mode lets it read data from
objects with attributes — the exact shape returned by SQLAlchemy, Tortoise,
or any hand-rolled ORM row.

## Key takeaways

- Enable with `model_config = ConfigDict(from_attributes=True)`.
- Validate with `Model.model_validate(orm_obj)` (v1: `from_orm`).
- In v1 this flag was named `orm_mode`; same behavior, renamed in v2.
- Works with nested relationships as long as they are accessible as attrs.

## When to use

- Converting SQLAlchemy rows into FastAPI response models.
- Anywhere the source is an object, not a mapping.

## Files

| File | Purpose |
|------|---------|
| `01_from_attributes.py` | Minimum working example with a fake ORM object. |
| `02_sqlalchemy_example.py` | FastAPI `response_model` pattern with SQLAlchemy. |
