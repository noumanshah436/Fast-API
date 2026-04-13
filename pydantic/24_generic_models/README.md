# 24. Generic Models

## ⚡ TL;DR
`typing.Generic` now works directly on `BaseModel` — one container schema,
many payload types. Parameterize at the call-site: `Page[User]`, `Response[Order]`.

## 🎯 When to use
- Paginated list endpoints (same shape, different item type)
- Consistent success/error envelopes across an API
- Task/result wrappers, cache entries, any reusable container

## v1 → v2 rename
| v1 | v2 |
|----|----|
| `from pydantic.generics import GenericModel` | `from typing import Generic, TypeVar` |
| `class Page(GenericModel, Generic[T])` | `class Page(BaseModel, Generic[T])` |

## Key points
- Inherit from both `BaseModel` **and** `Generic[T]`
- Pydantic builds a specialized validator per `Model[Concrete]`
- Specializations are cached — reuse is cheap
- Compose freely: `Response[Page[Order]]`

## ⚠️ Gotchas
| Pitfall | Fix |
|---------|-----|
| Forgetting `Generic[T]` | T becomes `Any`, no per-item validation |
| TypeVar defined inside class | Declare it at module level |
| `Optional[T]` without `= None` | v2 still requires an explicit default |

## Files
| File | Purpose |
|------|---------|
| `01_generic_model.py` | `Page[T]` pagination wrapper |
| `02_api_response_wrapper.py` | `Response[T]` envelope with status + data |
