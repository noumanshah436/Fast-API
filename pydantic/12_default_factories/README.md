# 12. Default Factories

⚡ **TL;DR** — `Field(default_factory=...)` produces a **fresh default per instance**. Use it for mutable containers and for values that must be computed at creation time (UUIDs, timestamps).

## 🎯 When to use

| Scenario                    | Factory                                                    |
|-----------------------------|------------------------------------------------------------|
| Empty collection            | `default_factory=list` / `dict` / `set`                    |
| Auto-generated ID           | `default_factory=uuid4`                                    |
| `created_at` / `updated_at` | `default_factory=lambda: datetime.now(timezone.utc)`       |
| Random token / secret       | `default_factory=secrets.token_urlsafe`                    |
| Copied literal              | `default_factory=lambda: {"v": 1}`                         |

## ⚠️ Gotchas

- Factory must be **zero-arg** — wrap args in a `lambda`.
- `= []` or `= datetime.now()` at class scope → evaluated **once**, shared.
- `datetime.utcnow` is deprecated; always use `datetime.now(timezone.utc)`.
- Caller-supplied values override the factory — round-trips work seamlessly.

## Files

| File                              | What it shows                                          |
|-----------------------------------|--------------------------------------------------------|
| `01_default_factory_basics.py`    | `list` / `dict` / literal-lambda factories             |
| `02_dynamic_defaults.py`          | `uuid4` + `datetime.now(timezone.utc)`                 |
