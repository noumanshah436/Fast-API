# 3. Validation Exceptions

> ⚡ **TL;DR** — Bad input raises `ValidationError`. It reports **all** failures at once, each with a structured `loc / msg / type / input`.

## 🎯 Anatomy of an error

| Key | Meaning | Use it for |
|---|---|---|
| `loc` | Tuple path to the bad field | `"address.zip_code"` display |
| `msg` | Human-readable reason | End-user message |
| `type` | Machine code (`missing`, `int_parsing`, …) | Branching / i18n keys |
| `input` | Offending value | Logs, debugging |
| `url` | Link to Pydantic docs | Optional |

## Useful methods on `ValidationError`

```python
e.error_count()     # int
e.errors()          # list[dict]  — programmatic
e.json(indent=2)    # str         — ready for HTTP 422 (FastAPI uses this)
```

## Three patterns you'll use

1. **try/except** at boundaries (HTTP handlers, CLIs, workers).
2. **safe_parse** → `(model, None) | (None, errors)` — Go/Rust-style results.
3. **to_api_errors** → `{field: msg}` — frontend-friendly shape.

## ⚠️ Gotchas

- Pydantic collects **all** errors before raising — don't assume the first one is the "real" one.
- Inside `@field_validator`, raise plain `ValueError` — Pydantic wraps it into `ValidationError` automatically. Never raise `ValidationError` by hand.
- `loc` is a **tuple**, not a string — join it for UI.

## Files

| File | Description |
|---|---|
| `01_validation_error.py` | Structure of ValidationError |
| `02_error_handling_patterns.py` | try/except · safe_parse · API formatting |
