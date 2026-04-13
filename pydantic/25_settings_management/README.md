# 25. Settings Management

Pydantic v2 split settings into a separate package:

```bash
pip install pydantic-settings
```

`BaseSettings` loads config from environment variables, `.env` files,
secrets directories, etc., with the same validation you already know.

## Key takeaways

- Import from `pydantic_settings`, not `pydantic`.
- Config lives in `SettingsConfigDict` (not the old inner `Class Config`).
- Env vars beat `.env` which beats defaults — last write wins.
- Use `env_nested_delimiter` to hydrate nested models from flat env vars.

## When to use

- Twelve-factor config for FastAPI / worker services.
- Anywhere you'd otherwise scatter `os.getenv` calls.

## Files

| File | Purpose |
|------|---------|
| `01_base_settings.py` | Load settings from process env vars. |
| `02_env_file.py` | `.env` file + `env_prefix` for namespacing. |
| `03_nested_settings.py` | Nested settings via `env_nested_delimiter`. |
