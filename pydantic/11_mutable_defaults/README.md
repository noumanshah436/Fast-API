# 11 - Mutable Defaults

The classic "shared list" bug that burns every Python dev once, and how
Pydantic handles it differently from dataclasses.

## Key takeaways

- A mutable default (list, dict, set) defined at class level is SHARED across
  all instances in plain Python / dataclasses -- mutating one mutates all.
- Dataclasses raise at class-definition time to stop this bug.
- Pydantic v2 deep-copies the default per instance, so it IS safe -- but
  relying on that is still bad style.
- Always use `Field(default_factory=list)` (or `dict`, `set`) for mutable
  defaults. Intent is explicit and behavior matches every Python codebase.

## When / why

- Any time a field's default is a list, dict, set, or custom mutable object.
- Pydantic models representing things like tags, scores, metadata dicts.

## Files

| File | What it shows |
|------|---------------|
| `01_mutable_default_pitfall.py` | The bug in a plain class, dataclass guard, Pydantic protection |
| `02_correct_pattern.py` | `default_factory=list` / `default_factory=dict` done right |
