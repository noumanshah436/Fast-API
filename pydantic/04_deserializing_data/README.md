# Topic 4: Deserializing Data

## What is Deserialization?

Deserialization is the process of converting raw data (dicts, JSON strings, etc.) into structured Pydantic model instances. This is one of the most common operations in real-world applications -- whenever you receive data from an API, a database, a config file, or user input, you need to parse it into a validated model.

## Key Methods

| Method | Input | Description |
|--------|-------|-------------|
| `Model(**data)` | keyword arguments | Standard constructor, validates each field |
| `model_validate(data)` | dict (or dict-like object) | Parse a dict into a model instance |
| `model_validate_json(json_str)` | JSON string | Parse a JSON string directly into a model |

## model_validate() vs Constructor

Both `User(name="Alice", age=30)` and `User.model_validate({"name": "Alice", "age": 30})` produce the same result. The difference:

- **Constructor**: Best when you already have individual values.
- **model_validate()**: Best when you have a dict (e.g., from a database row, another function, etc.).

## model_validate_json()

`model_validate_json()` parses a JSON string directly. This is faster than doing `json.loads()` followed by `model_validate()` because Pydantic can optimize the parsing internally.

## Handling Invalid Input

When deserialization fails, Pydantic raises `ValidationError` with details about every field that failed. You can:

1. Catch the error and inspect individual field errors.
2. Return user-friendly messages.
3. Use `strict=True` to disable type coercion during parsing.

## Files in This Section

| File | Description |
|------|-------------|
| `01_parsing_dict_to_model.py` | Parsing dicts into models with model_validate() |
| `02_parsing_json_to_model.py` | Parsing JSON strings with model_validate_json() |
| `03_handling_invalid_input.py` | Error scenarios and graceful handling |
