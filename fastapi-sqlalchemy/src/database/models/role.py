from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel


class Role(PostgresModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    slug = Column(String(80), nullable=False, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")
