"""
Dynamic defaults: UUIDs and timestamps
======================================
When the default must be computed at creation time.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    # Auto-assign a unique ID if the caller did not provide one.
    id: UUID = Field(default_factory=uuid4)
    # Capture *when this instance was built*, not when the class was defined.
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    name: str


e1 = Event(name="signup")
e2 = Event(name="checkout")

# Different IDs and (slightly) different timestamps -- factories ran twice.
print(e1.id != e2.id)                    # True
print(e1.created_at <= e2.created_at)    # True

# Caller can still override the default when replaying or importing data.
imported = Event(
    id="11111111-1111-1111-1111-111111111111",
    created_at="2026-01-01T00:00:00Z",
    name="import",
)
print(imported.model_dump_json())


# Anti-pattern: `created_at: datetime = datetime.now()` evaluates ONCE at
# class definition, so every Event shares the module-import timestamp.
