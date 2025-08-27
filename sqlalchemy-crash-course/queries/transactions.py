from main import session
from models.user import User, Preference

# Create a new user
user = User(
    first_name="John",
    last_name="Smith",
    email="jsmith@gmail.com",
)

session.add(user)

# Simulate an error during transaction
raise Exception("Something went wrong")

# This code won't execute due to the exception above
preference = Preference(
    language="English",
    currency="GBP",
)

preference.user = user
session.commit()
