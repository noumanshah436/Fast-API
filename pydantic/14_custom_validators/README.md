# 14. Custom Validators

Type checks are not enough -- you often need **domain rules** ("email must be
lowercase", "end after start", "password == password_confirm"). Pydantic v2
gives you `@field_validator` and `@model_validator` for that.

## Key Takeaways
- `@field_validator("field", mode="after")` -- runs AFTER type coercion;
  value is already the declared type. Use for single-field domain rules.
- `@field_validator("field", mode="before")` -- runs on the RAW input; use
  for preprocessing (strip, split, normalize).
- `@model_validator(mode="after")` -- cross-field checks on the fully built
  model (`self` is the validated instance).
- Raise `ValueError` / `AssertionError` -- Pydantic wraps it into a
  `ValidationError` with the correct `loc`.

## When to Use It
- Normalizing input (trim, lowercase, CSV -> list).
- Business rules a type alone cannot express.
- Consistency between fields (date ranges, matching passwords).

## Files
- `01_field_validator.py` -- single-field rules (`mode="after"`).
- `02_model_validator.py` -- cross-field rules.
- `03_before_vs_after.py` -- raw-input preprocessing vs post-type checks.
