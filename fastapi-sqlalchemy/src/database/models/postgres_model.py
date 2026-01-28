from datetime import UTC, datetime
from sqlalchemy import Column, DateTime, Integer
from src.database.config import Base


class PostgresModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(UTC), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    )
