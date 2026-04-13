# 27. Performance

## ⚡ TL;DR
v2's Rust core is **5-50x faster** than v1 by default. You still lose wins by double-validating data or parsing JSON the slow way (`json.loads` then `model_validate`).

## 🎯 When to care
- Request handlers on hot paths.
- Stream processors (Kafka, SQS, Kinesis) handling high-volume JSON bytes.
- Bulk importers / ETL running millions of rows through a model.

## 🔁 Cheat sheet

| Situation | Do this | Not this |
|-----------|---------|----------|
| Raw JSON bytes arriving | `Model.model_validate_json(raw)` | `model_validate(json.loads(raw))` |
| Already have a model    | Pass the instance         | `Model(**m.model_dump())` |
| Need a mutated copy     | `m.model_copy(update={...})` | re-validate from a dict |
| Output to wire          | `m.model_dump_json()`     | manual `json.dumps(asdict)` |

## ⚠️ Gotchas
- `model_dump()` is for output — avoid it inside hot internal paths.
- `model_construct()` skips validation entirely; only safe for trusted data.
- Re-validating already-typed data is the #1 performance anti-pattern in v2.

## Files

| File | Purpose |
|------|---------|
| `01_v2_speedup.py` | Where the speed comes from; illustrative sketch. |
| `02_avoid_reparsing.py` | Pass models, don't rebuild them. |
| `03_model_validate_json.py` | Parse JSON bytes in one pass. |
