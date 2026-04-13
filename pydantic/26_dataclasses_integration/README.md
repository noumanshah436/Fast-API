# 26. Dataclasses Integration

Pydantic ships a `@pydantic.dataclasses.dataclass` decorator that validates
fields on assignment while keeping the surface of a stdlib dataclass.

## Key takeaways

- Drop-in replacement for `@dataclass`, plus runtime validation.
- No `model_dump` / `model_validate` — use `dataclasses.asdict` / direct init.
- `BaseModel` has the richer API (serialization, JSON schema, aliases, etc.).
- Pydantic dataclasses interoperate with libraries that inspect `dataclasses.fields`.

## When to use

- Existing code already builds on stdlib dataclasses.
- You want validation without changing the call sites.
- Otherwise — prefer `BaseModel` for full feature parity.

## Files

| File | Purpose |
|------|---------|
| `01_pydantic_dataclass.py` | Validated dataclass vs `BaseModel` side-by-side. |
| `02_when_to_use.py` | Decision guide between the two. |
