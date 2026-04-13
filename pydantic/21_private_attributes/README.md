# 21. Private Attributes

## ⚡ TL;DR
Per-instance state that sits **outside** the field system — not validated,
not in `model_dump()`, not in the JSON schema. Declared with `PrivateAttr()`.

## 🎯 When to use
- Caches, memoized values, lazy clients (DB sessions, HTTP clients)
- Counters, internal flags, derived values the API must not expose
- Anything that must not round-trip through JSON

## Key points
- Declare with `PrivateAttr(default=...)` or `PrivateAttr(default_factory=...)`
- Leading underscore (`_x`) is the naming convention
- Initialize derived values in `model_post_init(self, __context)`
- Constructor kwargs for private attrs are **silently ignored**
- Bypasses `frozen=True` — still mutable on frozen models

## ⚠️ Gotchas
| Pitfall | Fix |
|---------|-----|
| `_x: int = 0` at class level | Use `PrivateAttr(default=0)` |
| Shared mutable default (`default={}`) | Use `default_factory=dict` |
| Expecting `Model(_calls=5)` to stick | Set it inside a method / `model_post_init` |
| Expecting it in schema docs | It's private — exclude by design |

## Files
| File | Topic |
|------|-------|
| `01_private_attr.py` | `PrivateAttr()` for internal state |
| `02_underscore_fields.py` | Underscore names + `model_post_init` |
