from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel

class Team(PostgresModel):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    memberships = relationship("Membership", back_populates="team")