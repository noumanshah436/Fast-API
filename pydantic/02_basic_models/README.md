# 2. Basic Models

> ⚡ **TL;DR** — Subclass `BaseModel`, declare typed fields, and you get validation, serialization, and schema generation for free.

## 🎯 Three ways to instantiate

```python
User(name="Alice", age=30)                    # kwargs
User(**{"name": "Alice", "age": 30})          # dict-spread
User.model_validate({"name": "Alice"})        # explicit verb, dynamic input
```

## Core methods

| Method | Purpose |
|---|---|
| `model_dump()` | Model → dict |
| `model_dump_json()` | Model → JSON string (native datetime/UUID) |
| `model_validate(data)` | dict → Model |
| `model_validate_json(raw)` | JSON string → Model |
| `model_json_schema()` | Generate JSON Schema |
| `model_copy(update={...})` | Copy with tweaks, no re-validation |
| `model_fields` | `{name: FieldInfo}` metadata |

## Filtering `model_dump(...)` output

| Flag | Use case |
|---|---|
| `include={"a","b"}` | Public whitelist |
| `exclude={"password_hash"}` | Strip secrets |
| `exclude_none=True` | PATCH / OpenAPI friendliness |
| `exclude_unset=True` | PATCH diffs — only what caller sent |
| `exclude_defaults=True` | Slim payloads |

## ⚠️ Gotchas

- `model_dump()` is **not** always JSON-safe (e.g. `datetime`). Use `model_dump_json()` or FastAPI's `jsonable_encoder`.
- Mutable defaults (`list[str] = []`) are safe in Pydantic — each instance gets its own copy.
- Prefer `model_copy` over direct mutation to keep value-object semantics.

## Files

| File | Description |
|---|---|
| `01_creating_models.py` | Field declaration, supported types, instantiation |
| `02_attribute_access.py` | Dot access, `model_fields`, `model_copy` |
| `03_serialization_basics.py` | `model_dump` / `model_dump_json`, include/exclude |
