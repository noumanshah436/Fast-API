"""
BaseSettings: validated env-var config
======================================
pydantic_settings is a SEPARATE package in v2:  pip install pydantic-settings
"""

import os
from pydantic import Field
from pydantic_settings import BaseSettings


# Simulate a real deployment environment.
os.environ["DATABASE_URL"] = "postgresql://user:pw@db/app"
os.environ["SECRET_KEY"] = "do-not-log-me"
os.environ["DEBUG"] = "false"


class AppSettings(BaseSettings):
    # Field names map to env vars case-insensitively by default.
    database_url: str
    secret_key: str = Field(min_length=8)   # validation still applies
    debug: bool = False                     # "false"/"0" coerced to bool


# Instantiate once at startup; inject everywhere else.
settings = AppSettings()
print(settings.model_dump())

# FastAPI pattern: use lru_cache so the env is parsed exactly once.
#
#   from functools import lru_cache
#   @lru_cache
#   def get_settings() -> AppSettings:
#       return AppSettings()
#
#   def handler(s: AppSettings = Depends(get_settings)): ...
