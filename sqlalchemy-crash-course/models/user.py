from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from models.base import TimeStampedModel, Model


class User(TimeStampedModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(320), nullable=False, unique=True)

    preference = Relationship("Preference", back_populates="user", uselist=False, passive_deletes=True)
    addresses = Relationship("Address", back_populates="user", passive_deletes=True)
    roles = Relationship("Role", secondary="user_roles", back_populates="users", passive_deletes=True)

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.first_name} {self.last_name}"

# **********************************************

# one-to-one relationship
# each user have only one preference
class Preference(TimeStampedModel):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(80), nullable=False)
    currency = Column(String(3), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = Relationship("User", back_populates="preference")

# **********************************************

# one-to-many relationship
# one user can have many addresses
class Address(TimeStampedModel):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    road_name = Column(String(80), nullable=False)
    postcode = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    user = Relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.city}"

# **********************************************

# many-to-many relationship
# one user can have many roles and also one role can belongs to many users
class Role(Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    slug = Column(String(80), nullable=False, unique=True)

    users = Relationship("User", secondary="user_roles", back_populates="roles", passive_deletes=True)
    # secondary is to define the join table

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.name}"


# joint table
class UserRole(TimeStampedModel):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

# **********************************************


# uselist:
# A boolean that indicates if this property should be loaded as a list or a scalar
# for one to one relatioonship, we will specify uselist=false

# ****************************************

# passive_deletes:

# In SQLAlchemy, passive_deletes is an option that you can set on a relationship to control whether or not the deletion of related objects is handled automatically by SQLAlchemy.

# By default, SQLAlchemy will handle the deletion of related objects according to the cascade rules specified. However, if you set passive_deletes=True, SQLAlchemy will not issue a DELETE statement for related objects when the parent object is deleted. Instead, it relies on the database to handle this deletion, which can be useful if you have database-level foreign key constraints with ON DELETE CASCADE.

# ****************************************

# secondary option is to define the join table in many-to-many relationship

# ****************************************

