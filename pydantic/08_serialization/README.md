# 08 - Serialization

Turning models back into dicts / JSON for responses, logs, and storage.

## Key takeaways

- `model_dump()` -> dict, `model_dump_json()` -> JSON string.
- `include` / `exclude` shape the output (nested via dict syntax).
- `exclude_none=True` drops null fields; `exclude_unset=True` drops fields the user never set.
- `by_alias=True` emits keys in the alias form (camelCase) for API responses.

## When / why

- Building FastAPI responses that should hide internal fields (e.g. password hashes).
- PATCH endpoints where you only want to send fields the client actually provided.
- Returning JSON that matches a frontend's expected camelCase shape.

## Files

| File | What it shows |
|------|---------------|
| `01_model_dump_basics.py` | `model_dump`, `model_dump_json`, nested models |
| `02_include_exclude.py` | `include`, `exclude`, `exclude_none`, `exclude_unset` |
| `03_by_alias.py` | `by_alias=True` for camelCase API responses |
