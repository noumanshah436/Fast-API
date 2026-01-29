from sqlalchemy import Column, String
from src.database.models.postgres_model import PostgresModel
from sqlalchemy.orm import relationship


class User(PostgresModel):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, nullable=False)

    posts = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    profile = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    roles = relationship("Role", secondary="user_roles", back_populates="users")
