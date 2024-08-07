from sqlalchemy import desc

from models.user import User, Role

all_users = User.query.all()
first_user = User.query.first()

print(all_users)

# ************************************

johns = User.query.filter_by(first_name="John").all()
johns = User.query.filter(User.first_name == "John").all()

gmail_users = User.query.filter(User.email.like("%@gmail.com")).all()

print(johns)
print(gmail_users)

# ************************************
# joins

super_admins = (
    User.query
    .join(User.roles)
    .filter(Role.slug == "super-admin")
    .all()
)

print(super_admins)

# ************************************
# ordering

users_by_name = (
    User.query
    .order_by(User.first_name)
    .all()
)

users_by_name_desc = (
    User.query
    .order_by(desc(User.first_name))
    .all()
)

#  if two user have same first_name, then it will order them by last_name
users_by_names_desc = (
    User.query
    .order_by(desc(User.first_name))
    .order_by(desc(User.last_name))
    .all()
)
# ************************************

first_three_users = User.query.limit(3).all()

# to skip first 3 users
skip_three_users = User.query.offset(3).all()

num_of_users = User.query.count()

print(num_of_users)
