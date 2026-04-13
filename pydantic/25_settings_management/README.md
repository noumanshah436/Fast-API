# 25. Settings Management

## ⚡ TL;DR
`BaseSettings` loads validated config from env vars, `.env` files, and secrets
dirs — same Pydantic validation, twelve-factor friendly. In v2 it lives in a
separate package: `pip install pydantic-settings`.

## 🎯 When to use
- FastAPI / worker service configuration
- Anywhere you'd otherwise scatter `os.getenv` + `int(...)` + `bool(...)`
- Multi-environment apps (dev / staging / prod) with `.env` files

## v1 → v2 rename
| v1 | v2 |
|----|----|
| `from pydantic import BaseSettings` | `from pydantic_settings import BaseSettings` |
| `class Config: env_prefix = "APP_"` | `model_config = SettingsConfigDict(env_prefix="APP_")` |

## Precedence (highest wins)
1. `AppSettings(debug=True)` — init kwargs
2. Real process env vars
3. `.env` file entries
4. Field defaults

## Key points
- Import from `pydantic_settings`, **not** `pydantic`
- Use `SettingsConfigDict` (not the old inner `class Config`)
- `env_prefix="APP_"` namespaces; field names stay unprefixed
- `env_nested_delimiter="__"` hydrates nested sub-models from flat env vars
- Wrap construction in `@lru_cache` so env is parsed once per process

## ⚠️ Gotchas
- Never commit real `.env` files — ship `.env.example`
- `extra="forbid"` at root can crash on unrelated OS env vars
- Boolean coercion only accepts `true/false/1/0/yes/no` — other strings raise

## Files
| File | Purpose |
|------|---------|
| `01_base_settings.py` | Load settings from process env vars |
| `02_env_file.py` | `.env` file + `env_prefix` for namespacing |
| `03_nested_settings.py` | Nested sub-models via `env_nested_delimiter` |
