"""
Nested settings via env_nested_delimiter
========================================
Group related config into sub-models; hydrate from flat env vars like
APP_DATABASE__URL, APP_DATABASE__POOL_SIZE.
"""

import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# Flat env vars -- the double-underscore descends into the nested model.
os.environ["APP_DATABASE__URL"] = "postgresql://prod/db"
os.environ["APP_DATABASE__POOL_SIZE"] = "20"
os.environ["APP_REDIS__URL"] = "redis://cache:6379/0"


class DatabaseSettings(BaseModel):
    # Plain BaseModel is fine for nested leaves -- no need for BaseSettings.
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
