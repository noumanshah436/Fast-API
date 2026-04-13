# Topic 3: Validation Exceptions

## ValidationError

When Pydantic cannot validate input data against the model's type hints and constraints, it raises a `ValidationError`. This is the primary exception you will work with in Pydantic.

Key characteristics:
- Pydantic collects **all** validation errors before raising, not just the first one.
- Each error includes the field location, a human-readable message, and an error type code.
- Errors can be accessed as Python dicts, JSON, or iterated over.

## Error Structure

Each error in a `ValidationError` contains:

| Key | Description |
|-----|-------------|
| `loc` | Tuple of field names showing the path to the error (e.g., `('address', 'zip_code')`) |
| `msg` | Human-readable error message |
| `type` | Machine-readable error type code (e.g., `int_parsing`, `missing`) |
| `input` | The value that caused the error |
| `url` | Link to documentation about the error type |

## How to Handle Errors

```python
from pydantic import BaseModel, ValidationError

try:
    user = User(name="Alice", age="bad")
except ValidationError as e:
    # Get error count
    print(e.error_count())

    # Iterate over errors
    for error in e.errors():
        print(error["loc"], error["msg"])

    # Get as JSON
    print(e.json())
```

## Common Patterns

1. **Try/Except** -- Catch `ValidationError` and format user-friendly messages.
2. **Safe Parse** -- Wrap `model_validate` to return `(model, None)` or `(None, errors)`.
3. **API Error Formatting** -- Convert errors into structured API response format.

## Custom Error Raising

Use `@field_validator` to add custom validation logic that raises `ValueError` with custom messages. Pydantic wraps these into `ValidationError` automatically.

## Files in This Section

| File | Description |
|------|-------------|
| `01_validation_error.py` | Understanding ValidationError structure |
| `02_error_handling_patterns.py` | Common patterns for handling errors |
