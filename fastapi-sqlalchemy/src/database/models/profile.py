from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel


# One User has one Profile
class Profile(PostgresModel):
    __tablename__ = "profiles"

    bio = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user = relationship("User", back_populates="profile")
