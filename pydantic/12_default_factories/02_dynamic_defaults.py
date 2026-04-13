"""
Dynamic defaults: UUIDs and timestamps
======================================
Use a factory when the default must be COMPUTED at instantiation, not class-load.

Cheat sheet
---------------------------------------------------------------------------
Field(default_factory=uuid.uuid4)                           unique id per row
Field(default_factory=lambda: datetime.now(timezone.utc))   fresh UTC stamp
Field(default_factory=secrets.token_urlsafe)                random token

Anti-pattern
- `created_at: datetime = datetime.now()` -> evaluated ONCE at class-load;
  every instance then shares the module-import timestamp.
- `datetime.utcnow` is naive and deprecated; use `datetime.now(timezone.utc)`.

FastAPI tip: factories still defer to caller-supplied values, so importing
historical records just passes `created_at=...` explicitly.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    # Lambda is required: we want `now(tz)` EACH call, not one shared moment.
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    name: str


e1 = Event(name="signup")
e2 = Event(name="checkout")
print(e1.id != e2.id, e1.created_at <= e2.created_at)   # True True

# Caller-supplied values always override the factory (replay / imports).
imported = Event(
    id="11111111-1111-1111-1111-111111111111",
    created_at="2026-01-01T00:00:00Z",
    name="import",
)
print(imported.model_dump_json())
