from sqlalchemy import Column, String
from src.database.models import PostgresModel


class User(PostgresModel):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, nullable=False)
