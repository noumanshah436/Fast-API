from blog.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Boolean,
    Numeric,
)
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


class UserType(enum.Enum):
    client = "client"
    freelancer = "freelancer"


class ProposalStatus(enum.Enum):
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    user_type = Column(Enum(UserType), nullable=False)

    # Relationships
    projects = relationship(
        "Project", back_populates="client", cascade="all, delete-orphan"
    )
    proposals = relationship(
        "Proposal", back_populates="freelancer", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    client = relationship("User", back_populates="projects")
    proposals = relationship(
        "Proposal", back_populates="project", cascade="all, delete-orphan"
    )


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bid_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.submitted)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="proposals")
    freelancer = relationship("User", back_populates="proposals")
    contract = relationship(
        "Contract",
        back_populates="proposal",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    proposal_id = Column(
        Integer, ForeignKey("proposals.id"), nullable=False, unique=True
    )
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Relationships
    proposal = relationship("Proposal", back_populates="contract")
    milestones = relationship(
        "Milestone", back_populates="contract", cascade="all, delete-orphan"
    )


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(DateTime, nullable=True)
    is_paid = Column(Boolean, default=False)

    # Relationships
    contract = relationship("Contract", back_populates="milestones")


# class Blog(Base):
#     __tablename__ = "blogs"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     body = Column(String)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     creator = relationship("User", back_populates="blogs")


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)

#     blogs = relationship("Blog", back_populates="creator")
