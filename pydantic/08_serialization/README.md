# 08 - Serialization

**⚡ TL;DR** — `model_dump()` → dict, `model_dump_json()` → str. Tweak with
`include`, `exclude`, `by_alias`, and the `exclude_*` family.

## Option cheatsheet

| Option               | Effect                                           |
|----------------------|--------------------------------------------------|
| `include={...}`      | whitelist                                        |
| `exclude={...}`      | blacklist                                        |
| `exclude_none=True`  | drop None-valued fields                          |
| `exclude_unset=True` | drop fields the caller never set (PATCH)         |
| `exclude_defaults`   | drop fields still at default                     |
| `by_alias=True`      | emit alias (camelCase) keys                      |
| `mode="json"`        | dict with JSON-safe values (datetime→str, etc.)  |

## 🎯 When to use what

- **API response, hiding secrets** → `exclude={"password_hash"}`
- **PATCH body → SQL UPDATE** → `exclude_unset=True`
- **JS client expects camelCase** → `by_alias=True` + `populate_by_name=True`
- **Logs / files** → `model_dump_json(indent=2)`

## ⚠️ Gotchas

- `exclude_unset` ≠ `exclude_none`. First = never provided; second = provided as None.
- Nested include/exclude takes a dict, not a set of dotted paths.
- `by_alias=True` on dump is independent of `populate_by_name` on input.

## Files

| File | Shows |
|------|-------|
| `01_model_dump_basics.py` | `model_dump` / `model_dump_json`, nested |
| `02_include_exclude.py` | shaping, `exclude_unset` / `exclude_none` |
| `03_by_alias.py` | camelCase wire format |
