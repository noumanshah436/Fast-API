from src.database.config import Base
from src.database.models.joined_table_inheritance import (
    Company,
    Employee,
    Engineer,
    Manager,
)
from src.database.models.single_table_inheritance import (
    CompanySTI,
    EmployeeSTI,
    ManagerSTI,
    EngineerSTI,
)
from src.database.models.many_to_many import Course, Student, StudentCourse
from src.database.models.post import Post
from src.database.models.role import Role
from src.database.models.user import User
from src.database.models.profile import Profile
from src.database.models.user_role import user_roles


__all__ = [
    "Base",
    "User",
    "Post",
    "Profile",
    "Role",
    "user_roles",
    "StudentCourse",
    "Student",
    "Course",
    # joined table inherotance tables
    "Company",
    "Employee",
    "Engineer",
    "Manager",
    # STI models
    "CompanySTI",
    "EmployeeSTI",
    "ManagerSTI",
    "EngineerSTI",
]
