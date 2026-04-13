# 24. Generic Models

Pydantic v2 supports `typing.Generic` directly on `BaseModel`. No more
`GenericModel` base class (that was v1). Useful for reusable wrappers:
pagination, API envelopes, task results.

## Key takeaways

- Inherit from both `BaseModel` and `Generic[T]`.
- Parameterize at use-site: `Page[User]`, `Response[Order]`.
- Full validation is generated per specialization.

## When to use

- Paginated list endpoints (same shape, different item type).
- Consistent success/error envelopes across an API.
- Any container schema that shouldn't be rewritten per payload type.

## Files

| File | Purpose |
|------|---------|
| `01_generic_model.py` | `Page[T]` pagination wrapper. |
| `02_api_response_wrapper.py` | `Response[T]` envelope with status + data. |
