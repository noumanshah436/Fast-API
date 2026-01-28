from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel

# One-to-Many Relationship

# One User can have many Posts, a post belongs to one User


class Post(PostgresModel):
    __tablename__ = "posts"

    title = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="posts",
    )
