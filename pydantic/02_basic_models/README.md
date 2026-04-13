# Topic 2: Basic Models

## BaseModel

`BaseModel` is the foundation class for all Pydantic models. Every model you create inherits from it and gains automatic validation, serialization, and schema generation.

## Type Hints

Pydantic uses standard Python type hints to define fields. Supported types include:

- **Basic types**: `str`, `int`, `float`, `bool`
- **Date/time**: `datetime`, `date`, `time`, `timedelta`
- **Collections**: `List`, `Dict`, `Set`, `Tuple`, `FrozenSet`
- **Special**: `UUID`, `Decimal`, `Enum`, `Path`
- **Optional**: `Optional[str]` (field can be `None`)
- **Nested models**: Other `BaseModel` subclasses

## Model Instantiation

Models can be created in three ways:

```python
# 1. Keyword arguments
user = User(name="Alice", age=30)

# 2. Dictionary unpacking
user = User(**{"name": "Alice", "age": 30})

# 3. model_validate (recommended for dicts)
user = User.model_validate({"name": "Alice", "age": 30})
```

## Attribute Access

Fields are accessed using dot notation: `user.name`, `user.age`. Nested models also use dot notation: `user.address.city`.

Use `model_fields` to introspect field definitions at runtime.

## Serialization Methods

| Method | Description |
|--------|-------------|
| `model_dump()` | Convert model to dictionary |
| `model_dump_json()` | Convert model to JSON string |
| `model_validate(data)` | Create model from dict |
| `model_validate_json(json_str)` | Create model from JSON string |
| `model_json_schema()` | Generate JSON Schema for the model |
| `model_copy(update={...})` | Create a copy with updated fields |

### Controlling Serialization Output

- `include` / `exclude` -- select specific fields
- `exclude_defaults` -- omit fields that equal their default value
- `exclude_none` -- omit fields that are `None`
- `exclude_unset` -- omit fields not explicitly set

## Files in This Section

| File | Description |
|------|-------------|
| `01_creating_models.py` | Model definition, instantiation, supported types |
| `02_attribute_access.py` | Dot notation, model_fields, immutability, model_copy |
| `03_serialization_basics.py` | model_dump, model_dump_json, include/exclude |
