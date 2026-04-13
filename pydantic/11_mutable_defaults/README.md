# 11. Mutable Defaults

⚡ **TL;DR** — A mutable default (`list`, `dict`, `set`) written at class level is ONE shared object in plain Python. Always write `Field(default_factory=list)`.

## 🎯 When to use

- Any field whose default is a `list`, `dict`, `set`, or custom mutable.
- Tags, scores, metadata dicts, error buckets, cached lookups.
- Auto-generated IDs and timestamps (see section 12).

## Behavior across frameworks

| Framework     | `items: list = []` | Outcome                                        |
|---------------|--------------------|------------------------------------------------|
| Plain class   | allowed            | ONE list shared across instances (silent bug)  |
| `@dataclass`  | rejected           | `ValueError` at class-definition time          |
| Pydantic v2   | allowed            | Deep-copied per instance (safe but poor style) |

## ⚠️ Gotchas

- Pydantic hiding the bug can mask issues once you port code to a `@dataclass`
  or plain class. Write `default_factory` **everywhere**.
- `datetime.utcnow` is deprecated — prefer `datetime.now(timezone.utc)`.
- Factories must be **zero-arg** callables (wrap args in a `lambda`).

## Files

| File                              | What it shows                                               |
|-----------------------------------|-------------------------------------------------------------|
| `01_mutable_default_pitfall.py`   | Shared-list bug, dataclass guard, Pydantic's auto-copy      |
| `02_correct_pattern.py`           | `Field(default_factory=list/dict/set)` the right way        |
