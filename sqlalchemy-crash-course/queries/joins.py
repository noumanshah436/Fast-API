from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload, joinedload
from models.user import User, Role, Address, Preference
from main import session

print("=" * 60)
print("SQLALCHEMY JOINS - FROM SIMPLE TO COMPLEX")
print("=" * 60)

# ============================================================
# 1. SIMPLE INNER JOIN
# ============================================================
print("\n1. SIMPLE INNER JOIN")
print("-" * 30)

# Get all users who have addresses
query = select(User).join(User.addresses)
users_with_addresses = session.execute(query).scalars().all()

print(f"Users with addresses: {len(users_with_addresses)}")
for user in users_with_addresses:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 2. LEFT JOIN (OUTER JOIN)
# ============================================================
print("\n2. LEFT JOIN (OUTER JOIN)")
print("-" * 30)

# Get all users and their addresses (including users without addresses)
query = select(User).outerjoin(User.addresses)
all_users_with_addresses = session.execute(query).scalars().all()

print(f"All users (including those without addresses): {len(all_users_with_addresses)}")
for user in all_users_with_addresses:
    address_count = len(user.addresses) if user.addresses else 0
    print(f"  - {user.first_name} {user.last_name}: {address_count} addresses")

# ============================================================
# 3. JOIN WITH FILTERING
# ============================================================
print("\n3. JOIN WITH FILTERING")
print("-" * 30)

# Get users who have addresses in London
query = select(User).join(User.addresses).where(Address.city == "London")
london_users = session.execute(query).scalars().all()

print(f"Users with London addresses: {len(london_users)}")
for user in london_users:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 4. MULTIPLE JOINS
# ============================================================
print("\n4. MULTIPLE JOINS")
print("-" * 30)

# Get users who have both addresses and roles
query = select(User).join(User.addresses).join(User.roles)
users_with_addresses_and_roles = session.execute(query).scalars().all()

print(f"Users with both addresses and roles: {len(users_with_addresses_and_roles)}")
for user in users_with_addresses_and_roles:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 5. JOIN WITH MULTIPLE CONDITIONS
# ============================================================
print("\n5. JOIN WITH MULTIPLE CONDITIONS")
print("-" * 30)

# Get users with admin role who have addresses in specific cities
query = (
    select(User)
    .join(User.roles)
    .join(User.addresses)
    .where(and_(
        Role.slug == "admin",
        Address.city.in_(["London", "New York", "Lahore"])
    ))
)
admin_users_in_cities = session.execute(query).scalars().all()

print(f"Admin users in specific cities: {len(admin_users_in_cities)}")
for user in admin_users_in_cities:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 6. SELF JOIN (JOINING TABLE TO ITSELF)
# ============================================================
print("\n6. SELF JOIN EXAMPLE")
print("-" * 30)

# Find users with the same first name (self join concept)
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
    .having(func.count(User.id) > 1)
)
duplicate_names = session.execute(query).all()

print("Users with duplicate first names:")
for name, count in duplicate_names:
    print(f"  - {name}: {count} users")

# ============================================================
# 7. COMPLEX JOIN WITH SUBQUERY
# ============================================================
print("\n7. COMPLEX JOIN WITH SUBQUERY")
print("-" * 30)

# Get users who have addresses in cities that other users also have addresses in
subquery = (
    select(Address.city)
    .group_by(Address.city)
    .having(func.count(Address.id) > 1)
    .scalar_subquery()
)

query = (
    select(User)
    .join(User.addresses)
    .where(Address.city.in_(subquery))
    .distinct()
)
users_in_popular_cities = session.execute(query).scalars().all()

print(f"Users in cities with multiple addresses: {len(users_in_popular_cities)}")
for user in users_in_popular_cities:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 8. CROSS JOIN EXAMPLE
# ============================================================
print("\n8. CROSS JOIN EXAMPLE")
print("-" * 30)

# Get all possible user-role combinations (simplified)
query = select(User.first_name, Role.name).select_from(User).join(User.roles)
user_role_combinations = session.execute(query).all()

print(f"All possible user-role combinations: {len(user_role_combinations)}")
for user_name, role_name in user_role_combinations[:5]:  # Show first 5
    print(f"  - {user_name} + {role_name}")

# ============================================================
# 9. ADVANCED: JOIN WITH AGGREGATION AND ORDERING
# ============================================================
print("\n9. ADVANCED: JOIN WITH AGGREGATION AND ORDERING")
print("-" * 30)

# Get users with their address count, ordered by address count
query = (
    select(
        User.first_name,
        User.last_name,
        func.count(Address.id).label('address_count')
    )
    .outerjoin(User.addresses)
    .group_by(User.id, User.first_name, User.last_name)
    .order_by(desc(func.count(Address.id)))
)
users_by_address_count = session.execute(query).all()

print("Users ordered by number of addresses:")
for first_name, last_name, count in users_by_address_count:
    print(f"  - {first_name} {last_name}: {count} addresses")

# ============================================================
# 10. COMPLEX: MULTIPLE JOINS WITH CONDITIONAL LOGIC
# ============================================================
print("\n10. COMPLEX: MULTIPLE JOINS WITH CONDITIONAL LOGIC")
print("-" * 30)

# Get users with specific criteria:
# - Have admin role OR super-admin role
# - Have addresses in UK (postcode starting with specific patterns)
# - Have preference for English language
query = (
    select(User)
    .join(User.roles)
    .join(User.addresses)
    .join(User.preference)
    .where(and_(
        or_(
            Role.slug == "admin",
            Role.slug == "super-admin"
        ),
        or_(
            Address.postcode.like("IG%"),
            Address.postcode.like("SW%"),
            Address.postcode.like("W%")
        ),
        Preference.language == "English"
    ))
)
complex_filtered_users = session.execute(query).scalars().all()

print(f"Users meeting complex criteria: {len(complex_filtered_users)}")
for user in complex_filtered_users:
    print(f"  - {user.first_name} {user.last_name}")

# ============================================================
# 11. ADVANCED: JOIN WITH WINDOW FUNCTIONS
# ============================================================
print("\n11. ADVANCED: JOIN WITH WINDOW FUNCTIONS")
print("-" * 30)

# Get users with their address count and simple ranking
query = (
    select(
        User.first_name,
        User.last_name,
        func.count(Address.id).label('address_count')
    )
    .outerjoin(User.addresses)
    .group_by(User.id, User.first_name, User.last_name)
    .order_by(desc(func.count(Address.id)))
)
users_with_rank = session.execute(query).all()

print("Users ordered by address count:")
for i, (first_name, last_name, count) in enumerate(users_with_rank, 1):
    print(f"  - Rank {i}: {first_name} {last_name} ({count} addresses)")

# ============================================================
# 12. ULTRA COMPLEX: MULTIPLE SUBQUERIES AND JOINS
# ============================================================
print("\n12. ULTRA COMPLEX: MULTIPLE SUBQUERIES AND JOINS")
print("-" * 30)

# Find users who have roles that are also assigned to users with London addresses
london_users_subquery = (
    select(User.id)
    .join(User.addresses)
    .where(Address.city == "London")
    .scalar_subquery()
)

london_user_roles_subquery = (
    select(Role.id)
    .join(Role.users)
    .where(User.id.in_(london_users_subquery))
    .scalar_subquery()
)

query = (
    select(User)
    .join(User.roles)
    .where(Role.id.in_(london_user_roles_subquery))
    .distinct()
)
users_sharing_roles_with_london_users = session.execute(query).scalars().all()

print(f"Users sharing roles with London users: {len(users_sharing_roles_with_london_users)}")
for user in users_sharing_roles_with_london_users:
    print(f"  - {user.first_name} {user.last_name}")

print("\n" + "=" * 60)
print("JOINS LEARNING COMPLETE!")
print("=" * 60)
