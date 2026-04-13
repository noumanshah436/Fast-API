# 28. JSON Schema

Every Pydantic model can emit a **JSON Schema** describing its fields, types,
constraints, and examples. This is the bridge to OpenAPI, FastAPI docs,
code generators, and frontend form builders.

## Key Takeaways
- `Model.model_json_schema()` returns a dict compatible with JSON Schema / OpenAPI.
- `Field(description=..., examples=[...])` metadata shows up in the schema.
- FastAPI uses this automatically for `/docs` (Swagger UI) and `/openapi.json`.
- No extra work: type hints + `Field(...)` are the single source of truth.

## When / Why
- Building APIs: auto-generated docs for consumers.
- Publishing a schema contract between services.
- Generating TypeScript/Go clients from your Python models.

## Files
- `01_model_json_schema.py` -- call `model_json_schema()`, inspect the output.
- `02_field_metadata_in_schema.py` -- how `description` and `examples` surface.
- `03_fastapi_integration.py` -- same schemas power FastAPI's `/docs`.
