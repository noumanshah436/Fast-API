from sqlalchemy import select
from sqlalchemy.orm import joinedload, subqueryload, contains_eager

from models.user import User, Address
from main import session

# Eager loading with join and filter
query = (
    select(User)
    .join(User.addresses)
    .where(Address.city == "London")
    .options(joinedload(User.addresses))
)

users = session.execute(query).scalars().all()

for user in users:
    print(user.addresses)