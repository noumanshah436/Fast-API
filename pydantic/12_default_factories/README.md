# 12. Default Factories

`Field(default_factory=...)` produces a **fresh default per instance**, avoiding
the classic "shared mutable default" bug and enabling dynamic values like
timestamps and UUIDs.

## Key Takeaways
- Use `default_factory` for any mutable default (`list`, `dict`, `set`).
- Also use it when the default must be computed at instantiation time
  (`datetime.now`, `uuid.uuid4`).
- The factory is a zero-arg callable; Pydantic calls it for each new model.
- Do **not** write `= []` or `= datetime.now()` at class scope -- both are
  evaluated once and shared.

## When to Use It
- Collection fields (tags, items, errors) that start empty.
- Auto-generated IDs for DB / API records.
- `created_at` / `updated_at` timestamps on request models.

## Files
- `01_default_factory_basics.py` -- mutable defaults done right.
- `02_dynamic_defaults.py` -- `uuid4` and `datetime.now` factories.
