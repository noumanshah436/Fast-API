from sqlalchemy import select
from main import session
from models.user import User

# Get the first user
query = select(User)
user = session.execute(query).scalar()

print(user)

# Delete the user
session.delete(user)
session.commit()

# Get the first user after deletion
query = select(User)
user = session.execute(query).scalar()

print(user)