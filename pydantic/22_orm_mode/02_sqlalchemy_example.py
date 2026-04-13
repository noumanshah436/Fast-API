"""
SQLAlchemy row -> FastAPI response_model
========================================
Canonical pattern: ORM model for persistence, Pydantic model for the wire.

Layering
--------
Layer           Object           Purpose
--------------------------------------------------------------
DB row          UserORM          persistence, includes secrets
Response DTO    UserRead         wire shape, secrets excluded
Endpoint        FastAPI          calls UserRead.model_validate(row)

FastAPI integration:
- Set `response_model=UserRead`
- Return the ORM row directly -- FastAPI calls `model_validate` for you
- Fields missing from the DTO are dropped (safe-by-default)

Gotchas:
- Without `from_attributes=True`, ORM rows fail validation with a type error
- `EmailStr` needs `pip install email-validator`
- Timezone-naive `datetime` from the DB can surprise JSON consumers —
  prefer `datetime.now(timezone.utc)` on the write path
"""

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, EmailStr


# Sketch of a SQLAlchemy row -- no real DB needed for the demo.
class UserORM:
    def __init__(self, id, email, is_active, created_at, hashed_password):
        self.id = id
        self.email = email
        self.is_active = is_active
        self.created_at = created_at
        self.hashed_password = hashed_password  # never leaves the server


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


# In FastAPI:
#   @app.get("/users/{uid}", response_model=UserRead)
#   def get_user(uid: int, db: Session = Depends(get_db)):
#       return db.get(UserORM, uid)

row = UserORM(
    id=42,
    email="alice@example.com",
    is_active=True,
    created_at=datetime.now(timezone.utc),
    hashed_password="$2b$12$notleaked",
)

# hashed_password excluded -- it's not in the DTO.
print(UserRead.model_validate(row).model_dump())
