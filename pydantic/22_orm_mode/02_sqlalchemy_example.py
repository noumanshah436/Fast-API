"""
SQLAlchemy row -> FastAPI response model
========================================
The canonical pattern: ORM model for persistence, Pydantic model for the wire.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


# --- Sketch of a SQLAlchemy model (no real DB needed for the example) ---
class UserORM:
    """Pretend this is `class UserORM(Base): __tablename__ = 'users'`."""
    def __init__(self, id, email, is_active, created_at, hashed_password):
        self.id = id
        self.email = email
        self.is_active = is_active
        self.created_at = created_at
        self.hashed_password = hashed_password  # never leaves the server


# --- Pydantic schema used as FastAPI's response_model ---
class UserRead(BaseModel):
    # from_attributes lets FastAPI serialize the ORM row directly.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


# --- Simulated endpoint ---
# In FastAPI you'd write:
#
#   @app.get("/users/{uid}", response_model=UserRead)
#   def get_user(uid: int, db: Session = Depends(get_db)):
#       return db.get(UserORM, uid)   # ORM row returned as-is
#
# FastAPI calls UserRead.model_validate(row) under the hood.

row = UserORM(
    id=42,
    email="alice@example.com",
    is_active=True,
    created_at=datetime(2026, 4, 13),
    hashed_password="$2b$12$notleaked",
)

payload = UserRead.model_validate(row).model_dump()
print(payload)  # hashed_password is excluded -- it isn't in the schema.
