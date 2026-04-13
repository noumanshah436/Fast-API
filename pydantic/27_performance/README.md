# 27. Performance

Pydantic v2's validation core (`pydantic-core`) is written in Rust. For most
workloads it's **5-50x faster** than v1 -- but you can still leave wins on the
table by double-validating data or parsing JSON the slow way.

## Key Takeaways
- v2 = Rust core. No config needed -- you already get the speedup.
- Don't re-validate trusted data: pass the `BaseModel` instance around.
- Avoid `Model(**existing.model_dump())` round-trips.
- Use `model_validate_json(raw_bytes)` instead of `json.loads` + `model_validate`.
- Parsing JSON directly skips the Python `dict` intermediate -- faster and less allocation.

## When / Why
- Hot paths: request handlers, stream processors, bulk importers.
- Anywhere you see the same object validated more than once.
- Ingestion endpoints that receive JSON bytes -- skip the manual `json.loads`.

## Files
- `01_v2_speedup.py` -- where the speed comes from; illustrative benchmark sketch.
- `02_avoid_reparsing.py` -- pass models, don't rebuild them.
- `03_model_validate_json.py` -- parse JSON in one step.
