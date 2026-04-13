"""
BaseSettings: validated env-var config
======================================
Twelve-factor config with Pydantic validation — parse env once at startup.

v1 vs v2
--------
v1                                    v2
-------------------------------------------------------------
from pydantic import BaseSettings    from pydantic_settings import BaseSettings
class Config: ...                    model_config = SettingsConfigDict(...)

Install:  pip install pydantic-settings  (separate package in v2)

Precedence (highest wins):
  init kwargs  >  real env vars  >  .env file  >  field defaults

Gotchas:
- Env var names are matched case-insensitively by default
- Booleans coerce from "true"/"false"/"1"/"0" -- other strings raise
- Validation errors at import time are good -- fail fast, fail loud
"""

import os
from pydantic import Field
from pydantic_settings import BaseSettings


# Pretend these were set by the deployment platform (systemd, k8s, etc.).
os.environ["DATABASE_URL"] = "postgresql://user:pw@db/app"
os.environ["SECRET_KEY"] = "do-not-log-me"
os.environ["DEBUG"] = "false"


class AppSettings(BaseSettings):
    # Field names map to env vars case-insensitively (DATABASE_URL == database_url).
    database_url: str
    secret_key: str = Field(min_length=8)   # validation runs just like any BaseModel
    debug: bool = False                     # "false"/"0"/"no" -> False


# Parse once at startup; every other module imports this singleton.
settings = AppSettings()
print(settings.model_dump())

# FastAPI pattern: cache so the env is parsed exactly once per process.
#
#   from functools import lru_cache
#   @lru_cache
#   def get_settings() -> AppSettings:
#       return AppSettings()
#
#   def handler(s: AppSettings = Depends(get_settings)): ...
