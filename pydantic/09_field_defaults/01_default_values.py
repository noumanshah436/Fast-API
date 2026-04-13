"""
Default values
==============
Direct assignment vs Field(default=...) -- same behavior, different ergonomics.
"""

from pydantic import BaseModel, Field


class Settings(BaseModel):
    # Plain form -- fine when you don't need metadata.
    debug: bool = False
    retries: int = 3

    # Field form -- identical default, but lets you add description/alias.
    # Reach for this once you want the value to show in OpenAPI docs.
    timeout: float = Field(default=5.0, description="HTTP timeout in seconds")
    log_level: str = Field(default="INFO", description="Python logging level")


s = Settings()
print(s.model_dump())
# {'debug': False, 'retries': 3, 'timeout': 5.0, 'log_level': 'INFO'}

# Overriding works the same either way.
s2 = Settings(debug=True, timeout=10.0)
print(s2.model_dump())

# Rule of thumb: start simple (plain assignment). Switch to Field(default=...)
# only when you also need description, alias, constraints, or examples.
