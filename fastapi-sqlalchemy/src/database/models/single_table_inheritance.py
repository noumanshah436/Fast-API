from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel


class CompanySTI(PostgresModel):
    __tablename__ = "company_sti"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    employees: Mapped[list["EmployeeSTI"]] = relationship(back_populates="company")


class EmployeeSTI(PostgresModel):
    __tablename__ = "employee_sti"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]  # <-- DISCRIMINATOR COLUMN
    company_id: Mapped[int] = mapped_column(ForeignKey("company_sti.id"))

    company: Mapped[CompanySTI] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "employee_sti",
    }


class ManagerSTI(EmployeeSTI):
    manager_data: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "manager_sti",
    }


class EngineerSTI(EmployeeSTI):
    engineer_info: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "engineer_sti",
    }
