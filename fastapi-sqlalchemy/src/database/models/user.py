from sqlalchemy import Column, String
from src.database.models.postgres_model import PostgresModel
from sqlalchemy.orm import relationship


class User(PostgresModel):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, nullable=False)

    posts = relationship("Post", back_populates="user")
