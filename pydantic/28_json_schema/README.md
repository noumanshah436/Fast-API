# 28. JSON Schema

## ⚡ TL;DR
Every `BaseModel` can emit a JSON Schema dict via `model_json_schema()` — the same format OpenAPI consumes. Type hints plus `Field(...)` metadata are the single source of truth for docs, code generators, and form builders.

## 🎯 When to use
- Building APIs that need auto-generated `/docs` (FastAPI reads this for free).
- Publishing a schema contract between services.
- Generating TypeScript / Go / Python clients from your models.
- Driving frontend form builders from the same types that validate the backend.

## 🔁 Cheat sheet

| Python type       | JSON Schema type            |
|-------------------|-----------------------------|
| `int`             | `integer`                   |
| `float`           | `number`                    |
| `str`             | `string`                    |
| `bool`            | `boolean`                   |
| `list[X]`         | `array` of X                |
| `dict`            | `object`                    |
| `Optional[X]`     | `anyOf: [X, null]`          |
| `Literal["a","b"]`| `enum: ["a", "b"]`          |
| Nested `BaseModel`| hoisted into `$defs` + `$ref` |

`Field(description=..., examples=[...], gt=0, min_length=3, ...)` — descriptions and constraints land straight in the schema and in Swagger UI.

## ⚠️ Gotchas
- Fields with a default are NOT in `required` — that is correct schema behaviour, double-check your defaults.
- Nested models appear under `$defs` and are referenced by `$ref`, not inlined.
- `examples` is plural (a list); `example` (singular) is legacy OpenAPI 3.0.
- Aliases vs field names: schema uses the alias by default; pass `by_alias=False` if you need field names.

## Files

| File | Purpose |
|------|---------|
| `01_model_json_schema.py` | Call `model_json_schema()` and inspect the output. |
| `02_field_metadata_in_schema.py` | How `description`, `examples`, constraints surface. |
| `03_fastapi_integration.py` | Same schemas power FastAPI's `/docs` automatically. |
