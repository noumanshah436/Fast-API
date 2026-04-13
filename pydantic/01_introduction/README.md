# 1. Introduction to Pydantic

> ⚡ **TL;DR** — Pydantic promotes Python type hints from documentation to **runtime validators**. Subclass `BaseModel`, get parsing, coercion, JSON (de)serialization, and JSON Schema for free.

## 🎯 When to use

- Parsing untrusted input: JSON APIs, webhooks, config files, CLI args
- The boundary between raw bytes and typed objects
- Anywhere you'd otherwise hand-roll `isinstance` / `try/except` checks

## ⚡ Why it exists

| Plain Python | Pydantic |
|---|---|
| Type hints ignored at runtime | Type hints **enforced** |
| Manual `isinstance` checks | Automatic + structured errors |
| `json.loads` → `dataclass(**d)` | `Model.model_validate_json(raw)` |
| No schema | `Model.model_json_schema()` |

## 🆚 vs `@dataclass`

| | `@dataclass` | `BaseModel` |
|---|---|---|
| Validation | none | full |
| Coercion | no | yes (lax by default) |
| Bad input | silently stored | `ValidationError` |
| JSON round-trip | manual | built-in |
| Use for | internal structs | app boundaries |

## ⚠️ Gotchas

- **v1 tutorials everywhere** — API was renamed in v2 (`.dict()` → `.model_dump()`, etc.). See `03_v1_vs_v2.py`.
- Coercion is **lax by default** (`"1"` → `1`). Pass `strict=True` to disable.
- `Optional[X]` means "can be None", **not** "can be omitted". Defaults decide presence.

## Files

| File | Description |
|---|---|
| `01_what_is_pydantic.py` | Minimal example + why it exists |
| `02_pydantic_vs_dataclasses.py` | Validation is the differentiator |
| `03_v1_vs_v2.py` | API renames you'll hit in old tutorials |
