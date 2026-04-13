"""
Default values
==============
Two equivalent ways, one with room for metadata.

Form                                     When to prefer
--------------------------------------------------------------------
x: int = 0                               simple, clean
x: int = Field(default=0)                + description / alias / examples
x: list[int] = Field(default_factory=list)   mutable defaults (always factory!)
x: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

⚠️ Never write `x: list[int] = []` -- Pydantic copies but you'll still trip on
   the pattern elsewhere. Use default_factory for lists, dicts, datetimes.
"""

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Settings(BaseModel):
    debug: bool = False
    retries: int = 3
    timeout: float = Field(default=5.0, description="HTTP timeout (s)")
    log_level: str = Field(default="INFO", description="Python logging level")
    # Mutable / time-based defaults must go through default_factory.
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


print(Settings().model_dump())
print(Settings(debug=True, timeout=10.0).model_dump())
