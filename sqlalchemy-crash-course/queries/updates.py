from sqlalchemy import select, update
from main import session
from models.user import Preference, User

# Get user preference by joining with user and filtering by email
query = (
    select(Preference)
    .join(Preference.user)
    .where(User.email == "johndoe@gmail.com")
)
user_preference = session.execute(query).scalar()

# Update the preference
user_preference.currency = "GBP"
session.commit()

# Update user email using update statement
query = (
    update(User)
    .where(User.first_name == "John")
    .where(User.last_name == "Doe")
    .values(email="johndoe@hotmail.com")
)
session.execute(query)

session.commit()

# print(user.email)
