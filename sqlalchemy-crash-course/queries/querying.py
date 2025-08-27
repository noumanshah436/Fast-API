from sqlalchemy import desc, select, func
from sqlalchemy.orm import selectinload

from models.user import User, Role
from main import session

# Get all users from the database
query = select(User)
all_users = session.execute(query).scalars().all()
print(all_users)

# Get the first user from the database (inefficient)
query = select(User)
first_user = session.execute(query).scalar()

# Get the first user from the database (efficient)
query = select(User).limit(1)
first_user = session.execute(query).scalar()

print(first_user)


# ************************************

# Find all users with first name "John"
query = select(User).where(User.first_name == "John")
johns = session.execute(query).scalars().all()

# Alternative way to filter users with first name "John"
query = select(User).filter(User.first_name == "John")
johns_alt = session.execute(query).scalars().all()

# Find all users with Gmail email addresses
query = select(User).where(User.email.like("%@gmail.com"))
gmail_users = session.execute(query).scalars().all()

print(johns)
print(gmail_users)

# ************************************
# joins

# Find all users who have the "super-admin" role (using join)
query = select(User).join(User.roles).where(Role.slug == "super-admin")
super_admins = session.execute(query).scalars().all()

print(super_admins)

# raw sql:

# SELECT * FROM users 
# JOIN user_roles AS user_roles_1 ON users.id = user_roles_1.user_id 
# JOIN roles ON roles.id = user_roles_1.role_id 
# WHERE roles.slug = 'super-admin'

# ************************************
# ordering

# Get all users ordered by first name (ascending)
query = select(User).order_by(User.first_name)
users_by_name = session.execute(query).scalars().all()

# Get all users ordered by first name (descending)
query = select(User).order_by(desc(User.first_name))
users_by_name_desc = session.execute(query).scalars().all()

# Get all users ordered by first name (descending), then by last name (descending)
# If two users have the same first name, they will be ordered by last name
query = select(User).order_by(desc(User.first_name)).order_by(desc(User.last_name))
users_by_names_desc = session.execute(query).scalars().all()

# ************************************

# Get only the first 3 users
query = select(User).limit(3)
first_three_users = session.execute(query).scalars().all()

# Skip the first 3 users and get the rest
query = select(User).offset(3)
skip_three_users = session.execute(query).scalars().all()

# Count the total number of users in the database
query = select(func.count(User.id))
num_of_users = session.execute(query).scalar()

print(num_of_users)
