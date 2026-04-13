# 30. Testing Pydantic Models

Pydantic models are easy to test because validation is deterministic:
good input constructs, bad input raises `ValidationError`. Use pytest
to pin both paths and the exact error details.

## Key Takeaways
- Happy path: `assert Model(**valid).field == expected`.
- Failure path: `with pytest.raises(ValidationError):`.
- Assert on `e.value.errors()` for specific `type` / `loc` -- not the message string.
- Use a **factory function** to build valid baselines and override just the field under test.

## When / Why
- Locking in business rules (validators) against regressions.
- Catching breaking schema changes before they hit production.
- Keeping tests concise when models have many required fields.

## Files
- `01_testing_validation.py` -- happy and sad path basics with pytest.
- `02_testing_error_details.py` -- assert on `type` and `loc` in `errors()`.
- `03_factory_pattern.py` -- `make_user(**overrides)` for clean fixtures.
