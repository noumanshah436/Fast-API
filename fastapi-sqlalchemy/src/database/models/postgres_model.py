from datetime import UTC, datetime
from typing import override
from sqlalchemy import Column, DateTime, Identity, Integer, inspect
from src.database.config import Base


class PostgresModel(Base):
    __abstract__ = True

    id = Column(Integer, Identity(), primary_key=True)

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
        # automatically prints all columns only
        try:
            columns = self.__table__.columns.keys()
        except AttributeError:
            # fallback if __table__ not yet defined
            columns = []

        attrs = ", ".join(f"{c}={getattr(self, c, None)!r}" for c in columns)
        return f"<{self.__class__.__name__} {attrs}>"

    # @override
    # def __repr__(self) -> str:
    #     """It only prints attributes that actually exist on the Python class, not every table column."""
    #     mapper = inspect(self.__class__)
    #     attrs = ", ".join(
    #         f"{attr.key}={getattr(self, attr.key, None)!r}"
    #         for attr in mapper.attrs
    #         if hasattr(self, attr.key)
    #     )
    #     return f"<{self.__class__.__name__} {attrs}>"

    # @override
    # def __repr__(self) -> str:
    #     # automatically prints all columns
    #     attrs = ", ".join(
    #         f"{c}={getattr(self, c)!r}" for c in self.__table__.columns.keys()
    #     )
    #     return f"<{self.__class__.__name__} {attrs}>"
