"""
.env files and env_prefix
=========================
Local dev config without polluting the shell; prefixes keep teams from colliding.

SettingsConfigDict knobs
------------------------
Key                     Effect
-------------------------------------------------------------
env_file                path to a .env to load
env_file_encoding       file encoding (usually "utf-8")
env_prefix              only consume vars starting with this prefix
case_sensitive          default False -- DB_URL == db_url
extra                   "ignore" | "forbid" | "allow" unknown keys

Precedence (highest wins):
  init kwargs  >  real env vars  >  .env file  >  defaults

Gotchas:
- Never commit real .env files -- ship .env.example instead
- With a prefix, FIELD names stay unprefixed (env APP_DEBUG -> field `debug`)
- `extra="forbid"` on BaseSettings will crash on unrelated OS env vars
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Write a demo .env next to this file so the script is self-contained.
env_path = Path(__file__).with_name(".env.example")
env_path.write_text(
    "APP_DATABASE_URL=postgresql://localhost/dev\n"
    "APP_SECRET_KEY=local-dev-secret\n"
    "APP_DEBUG=true\n"
)


class AppSettings(BaseSettings):
    # v2 config: SettingsConfigDict replaces the v1 inner `class Config`.
    model_config = SettingsConfigDict(
        env_file=str(env_path),
        env_file_encoding="utf-8",
        env_prefix="APP_",      # only APP_*-prefixed vars feed this model
        extra="ignore",         # tolerate unrelated OS env vars
    )

    # Field names are UNPREFIXED -- the prefix is stripped during lookup.
    database_url: str
    secret_key: str
    debug: bool = False


settings = AppSettings()
print(settings.model_dump())
