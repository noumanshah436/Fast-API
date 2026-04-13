# 26. Dataclasses Integration

## ⚡ TL;DR
`@pydantic.dataclasses.dataclass` gives you a stdlib-compatible dataclass with runtime validation. Use it for interop with code that inspects `dataclasses.fields` — otherwise reach for `BaseModel`.

## 🎯 When to use
- Third-party library iterates `dataclasses.fields(obj)` or calls `asdict`.
- Adding validation to an existing dataclass-based codebase without churn.
- You want `is_dataclass(obj) == True` but with type checking.

## 🔁 Cheat sheet

| Need                          | Pick                       |
|-------------------------------|----------------------------|
| HTTP / JSON / OpenAPI         | `BaseModel`                |
| `model_dump`, aliases, schema | `BaseModel`                |
| Stdlib dataclass interop      | `@pydantic_dataclass`      |
| Trusted internal data         | stdlib `@dataclass`        |

## ⚠️ Gotchas
- No `model_dump` / `model_validate` on a pydantic dataclass — use `dataclasses.asdict` and call the constructor directly.
- No `model_json_schema()` — if you need a schema, switch to `BaseModel`.
- Mixing stdlib and pydantic dataclasses in inheritance trees is brittle. Don't.

## Files

| File | Purpose |
|------|---------|
| `01_pydantic_dataclass.py` | Validated dataclass vs `BaseModel` side-by-side. |
| `02_when_to_use.py` | Decision tree between the three options. |
