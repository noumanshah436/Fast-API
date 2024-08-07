from main import session
from models.user import User, Role, Address, Preference

admin_role = Role.query.filter(Role.slug == "admin").first()

user = User(
    first_name="John",
    last_name="Smith",
    email="johnsmith@gmail.com"
)

session.add(user)
# ********************************

user2 = User()
user2.first_name = "Jane"
user2.last_name = "Doe"
user2.email = "janedoe@gmail.com"

session.add(user2)

# ********************************
user3 = User(
    first_name="Syed",
    last_name="Nouman",
    email="nouman@gmail.com",
)

user3.roles.append(admin_role)
user3.addresses.append(
    Address(
        road_name="sher shah road",
        postcode="IG114XE",
        city="Lahore",
    )
)
user3.preference = Preference(
    language="Urdu",
    currency="PKR"
)

session.add(user3)

session.commit()
