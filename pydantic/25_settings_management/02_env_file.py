"""
.env files and env_prefix
=========================
Load a .env during local dev; prefix keys to avoid collisions.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Write a sample .env next to this file so the example is self-contained.
env_path = Path(__file__).with_name(".env.example")
env_path.write_text(
    "APP_DATABASE_URL=postgresql://localhost/dev\n"
    "APP_SECRET_KEY=local-dev-secret\n"
    "APP_DEBUG=true\n"
)


class AppSettings(BaseSettings):
    # v2 config: SettingsConfigDict (replaces v1's inner `class Config`).
    model_config = SettingsConfigDict(
        env_file=str(env_path),
        env_file_encoding="utf-8",
        env_prefix="APP_",      # only vars starting with APP_ are consumed
        extra="ignore",         # unknown env vars don't blow up startup
    )

    database_url: str
    secret_key: str
    debug: bool = False


settings = AppSettings()
print(settings.model_dump())

# Precedence (highest wins): init kwargs > real env vars > .env > defaults.
