# 4. Deserializing Data

> ⚡ **TL;DR** — Deserialization is "raw input → validated model". Three entry points: the constructor, `model_validate()`, `model_validate_json()` — all share the same validation pipeline.

## 🎯 Pick the right entry point

| Call | Input | When to use |
|---|---|---|
| `Model(**data)` | kwargs | You already hold named values |
| `Model.model_validate(data)` | dict (or ORM row with `from_attributes`) | Dynamic / nested / non-identifier keys |
| `Model.model_validate_json(raw)` | `str` or `bytes` | JSON body, Kafka msg, file on disk — **preferred over `json.loads` + `model_validate`** |

## ⚡ Why `model_validate_json` > `json.loads` + `model_validate`

- Parsing happens inside Rust core — no intermediate Python `dict`
- One call, one try/except
- JSON syntax errors become `ValidationError(type="json_invalid")` — uniform shape

## Lax vs strict coercion

| Mode | `"1"` → `int` | `"true"` → `bool` | When |
|---|---|---|---|
| lax (default) | ✅ | ✅ | HTTP, CLI, forms — messy input |
| `strict=True` | ❌ | ❌ | Trusted upstream (Protobuf, internal RPC) |

Scope `strict` per call (`model_validate(data, strict=True)`) or model-wide (`ConfigDict(strict=True)`).

## ⚠️ Gotchas

- Constructor and `model_validate` run the **same** pipeline — pick for readability, not behaviour.
- `"yes"` / `"no"` are **not** coerced to `bool`; `"true"` / `"false"` / `0` / `1` are.
- A bad JSON string raises `ValidationError`, **not** `json.JSONDecodeError` — catch the right thing.

## Files

| File | Description |
|---|---|
| `01_parsing_dict_to_model.py` | `Model(**d)` vs `model_validate(d)` |
| `02_parsing_json_to_model.py` | `model_validate_json` + benchmark vs two-step |
| `03_handling_invalid_input.py` | json_invalid · lax coercion · `strict=True` |
