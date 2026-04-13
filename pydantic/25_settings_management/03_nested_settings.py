"""
Nested settings via env_nested_delimiter
========================================
Group related config into sub-models; hydrate from flat env vars.

Mapping rules
-------------
Env var                       Field path
-------------------------------------------------------------
APP_DATABASE__URL             settings.database.url
APP_DATABASE__POOL_SIZE       settings.database.pool_size
APP_REDIS__URL                settings.redis.url
APP_DEBUG                     settings.debug

Why nested?
- Organization: group related keys (database.*, redis.*) instead of flat sprawl
- Reusability: pass `settings.database` alone into a DB layer
- Validation scope: per-subsystem Pydantic models catch misconfig early

Gotchas:
- Leaf models can be plain `BaseModel` -- no need for BaseSettings everywhere
- The delimiter is conventionally `__` (double underscore); pick something
  your deploy tooling won't mangle
- Prefix strips FIRST, then delimiter splits -- APP_DATABASE__URL works
"""

import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# Flat env vars; `__` descends into the nested sub-model.
os.environ["APP_DATABASE__URL"] = "postgresql://prod/db"
os.environ["APP_DATABASE__POOL_SIZE"] = "20"
os.environ["APP_REDIS__URL"] = "redis://cache:6379/0"


class DatabaseSettings(BaseModel):
    # Plain BaseModel works for leaves -- only the root needs BaseSettings.
    url: str
    pool_size: int = 5


class RedisSettings(BaseModel):
    url: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",   # APP_DATABASE__URL -> database.url
    )

    database: DatabaseSettings
    redis: RedisSettings
    debug: bool = False


settings = AppSettings()
print(settings.model_dump())
print("db pool:", settings.database.pool_size)
