from datetime import UTC, datetime
from typing import override
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

    @override
    def __repr__(self) -> str:
        # automatically prints all columns
        attrs = ", ".join(
            f"{c}={getattr(self, c)!r}" for c in self.__table__.columns.keys()
        )
        return f"<{self.__class__.__name__} {attrs}>"
