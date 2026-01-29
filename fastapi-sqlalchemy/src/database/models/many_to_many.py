from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.models.postgres_model import PostgresModel


class StudentCourse(PostgresModel):
    __tablename__ = "student_courses"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    enrolled_at = Column(DateTime(timezone=True), nullable=False)

    student = relationship("Student", back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")


class Student(PostgresModel):
    __tablename__ = "students"

    name = Column(String, nullable=False)

    student_courses = relationship(
        "StudentCourse", back_populates="student", cascade="all, delete-orphan"
    )

    courses = relationship("Course", secondary="student_courses", viewonly=True)


class Course(PostgresModel):
    __tablename__ = "courses"

    title = Column(String, nullable=False)

    student_courses = relationship(
        "StudentCourse", back_populates="course", cascade="all, delete-orphan"
    )

    students = relationship("Student", secondary="student_courses", viewonly=True)
