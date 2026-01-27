from sqlalchemy import select, and_, or_, not_, func, desc, asc, distinct, case, cast, String, Integer, Boolean
from sqlalchemy.orm import selectinload, joinedload, subqueryload, contains_eager
from models.user import User, Role, Address, Preference
from main import session

print("=" * 70)
print("SQLALCHEMY 2.0 QUERY METHODS - COMPLETE REFERENCE")
print("=" * 70)

# ============================================================
# 1. BASIC SELECT METHODS
# ============================================================
print("\n1. BASIC SELECT METHODS")
print("-" * 40)

# Basic select with all columns
query = select(User)
all_users = session.execute(query).scalars().all()
print(f"All users: {len(all_users)}")

# Select specific columns
query = select(User.first_name, User.last_name, User.email)
user_data = session.execute(query).all()
print(f"User data (first 3): {user_data[:3]}")

# Select with alias
from sqlalchemy import alias
user_alias = alias(User, name="u")
query = select(user_alias.c.first_name, user_alias.c.last_name)
aliased_users = session.execute(query).all()
print(f"Aliased users (first 3): {aliased_users[:3]}")

# ============================================================
# 2. FILTERING METHODS
# ============================================================
print("\n2. FILTERING METHODS")
print("-" * 40)

# Basic WHERE clause
query = select(User).where(User.first_name == "John")
johns = session.execute(query).scalars().all()
print(f"Users named John: {len(johns)}")

# Multiple conditions with AND
query = select(User).where(
    and_(
        User.first_name == "John",
        User.last_name == "Doe"
    )
)
john_does = session.execute(query).scalars().all()
print(f"Users named John Doe: {len(john_does)}")

# Multiple conditions with OR
query = select(User).where(
    or_(
        User.first_name == "John",
        User.first_name == "Jane"
    )
)
johns_and_janes = session.execute(query).scalars().all()
print(f"Users named John or Jane: {len(johns_and_janes)}")

# NOT condition
query = select(User).where(not_(User.first_name == "John"))
non_johns = session.execute(query).scalars().all()
print(f"Users not named John: {len(non_johns)}")

# ============================================================
# 3. COMPARISON OPERATORS
# ============================================================
print("\n3. COMPARISON OPERATORS")
print("-" * 40)

# Equal
query = select(User).where(User.first_name == "John")
print(f"Equal to 'John': {session.execute(query).scalars().all().__len__()}")

# Not equal
query = select(User).where(User.first_name != "John")
print(f"Not equal to 'John': {session.execute(query).scalars().all().__len__()}")

# Greater than (for numeric fields)
query = select(User).where(User.id > 5)
print(f"Users with ID > 5: {session.execute(query).scalars().all().__len__()}")

# Less than or equal
query = select(User).where(User.id <= 5)
print(f"Users with ID <= 5: {session.execute(query).scalars().all().__len__()}")

# Between
query = select(User).where(User.id.between(1, 5))
print(f"Users with ID between 1-5: {session.execute(query).scalars().all().__len__()}")

# ============================================================
# 4. STRING OPERATIONS
# ============================================================
print("\n4. STRING OPERATIONS")
print("-" * 40)

# LIKE with wildcards
query = select(User).where(User.first_name.like("J%"))
j_names = session.execute(query).scalars().all()
print(f"Names starting with 'J': {len(j_names)}")

# ILIKE (case insensitive LIKE)
query = select(User).where(User.first_name.ilike("j%"))
j_names_insensitive = session.execute(query).scalars().all()
print(f"Names starting with 'j' (case insensitive): {len(j_names_insensitive)}")

# Contains
query = select(User).where(User.email.contains("gmail"))
gmail_users = session.execute(query).scalars().all()
print(f"Gmail users: {len(gmail_users)}")

# Starts with
query = select(User).where(User.first_name.startswith("J"))
j_start_names = session.execute(query).scalars().all()
print(f"Names starting with 'J': {len(j_start_names)}")

# Ends with
query = select(User).where(User.email.endswith(".com"))
com_users = session.execute(query).scalars().all()
print(f"Users with .com email: {len(com_users)}")

# ============================================================
# 5. IN AND NOT IN OPERATIONS
# ============================================================
print("\n5. IN AND NOT IN OPERATIONS")
print("-" * 40)

# IN operator
query = select(User).where(User.first_name.in_(["John", "Jane", "Bob"]))
specific_names = session.execute(query).scalars().all()
print(f"Users with specific names: {len(specific_names)}")

# NOT IN operator
query = select(User).where(User.first_name.not_in(["John", "Jane"]))
other_names = session.execute(query).scalars().all()
print(f"Users with other names: {len(other_names)}")

# IN with subquery
subquery = select(Address.user_id).where(Address.city == "London")
query = select(User).where(User.id.in_(subquery))
london_users = session.execute(query).scalars().all()
print(f"Users with London addresses: {len(london_users)}")

# ============================================================
# 6. NULL OPERATIONS
# ============================================================
print("\n6. NULL OPERATIONS")
print("-" * 40)

# IS NULL
query = select(User).where(User.first_name.is_(None))
null_names = session.execute(query).scalars().all()
print(f"Users with NULL first names: {len(null_names)}")

# IS NOT NULL
query = select(User).where(User.first_name.is_not(None))
non_null_names = session.execute(query).scalars().all()
print(f"Users with non-NULL first names: {len(non_null_names)}")

# ============================================================
# 7. ORDERING METHODS
# ============================================================
print("\n7. ORDERING METHODS")
print("-" * 40)

# ORDER BY ascending
query = select(User).order_by(User.first_name)
asc_users = session.execute(query).scalars().all()
print(f"Users ordered by first name (asc): {[u.first_name for u in asc_users[:3]]}")

# ORDER BY descending
query = select(User).order_by(desc(User.first_name))
desc_users = session.execute(query).scalars().all()
print(f"Users ordered by first name (desc): {[u.first_name for u in desc_users[:3]]}")

# Multiple ORDER BY
query = select(User).order_by(User.first_name, User.last_name)
multi_ordered = session.execute(query).scalars().all()
print(f"Users ordered by first name, then last name: {len(multi_ordered)}")

# ============================================================
# 8. LIMIT AND OFFSET
# ============================================================
print("\n8. LIMIT AND OFFSET")
print("-" * 40)

# LIMIT
query = select(User).limit(3)
limited_users = session.execute(query).scalars().all()
print(f"First 3 users: {len(limited_users)}")

# OFFSET
query = select(User).offset(3)
offset_users = session.execute(query).scalars().all()
print(f"Users after offset 3: {len(offset_users)}")

# LIMIT and OFFSET together (pagination)
query = select(User).limit(2).offset(2)
paginated_users = session.execute(query).scalars().all()
print(f"Paginated users (limit 2, offset 2): {len(paginated_users)}")

# ============================================================
# 9. AGGREGATION FUNCTIONS
# ============================================================
print("\n9. AGGREGATION FUNCTIONS")
print("-" * 40)

# COUNT
query = select(func.count(User.id))
total_users = session.execute(query).scalar()
print(f"Total users: {total_users}")

# COUNT DISTINCT
query = select(func.count(distinct(User.first_name)))
unique_names = session.execute(query).scalar()
print(f"Unique first names: {unique_names}")

# MAX
query = select(func.max(User.id))
max_id = session.execute(query).scalar()
print(f"Maximum user ID: {max_id}")

# MIN
query = select(func.min(User.id))
min_id = session.execute(query).scalar()
print(f"Minimum user ID: {min_id}")

# AVG (for numeric fields)
query = select(func.avg(User.id))
avg_id = session.execute(query).scalar()
print(f"Average user ID: {avg_id}")

# SUM
query = select(func.sum(User.id))
sum_ids = session.execute(query).scalar()
print(f"Sum of user IDs: {sum_ids}")

# ============================================================
# 10. GROUP BY AND HAVING
# ============================================================
print("\n10. GROUP BY AND HAVING")
print("-" * 40)

# GROUP BY
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
)
name_counts = session.execute(query).all()
print(f"Name counts: {name_counts}")

# GROUP BY with HAVING
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
    .having(func.count(User.id) > 1)
)
duplicate_names = session.execute(query).all()
print(f"Duplicate names: {duplicate_names}")

# Multiple GROUP BY columns
query = (
    select(User.first_name, User.last_name, func.count(User.id).label('count'))
    .group_by(User.first_name, User.last_name)
)
full_name_counts = session.execute(query).all()
print(f"Full name counts (first 3): {full_name_counts[:3]}")

# ============================================================
# 11. CASE STATEMENTS
# ============================================================
print("\n11. CASE STATEMENTS")
print("-" * 40)

# Simple CASE
query = (
    select(
        User.first_name,
        case(
            (User.first_name == "John", "Johnny"),
            (User.first_name == "Jane", "Janey"),
            else_="Other"
        ).label('nickname')
    )
)
nicknames = session.execute(query).all()
print(f"Nicknames (first 5): {nicknames[:5]}")

# CASE with multiple conditions
query = (
    select(
        User.first_name,
        case(
            (User.id <= 3, "Early User"),
            (User.id <= 6, "Mid User"),
            else_="Late User"
        ).label('user_category')
    )
)
user_categories = session.execute(query).all()
print(f"User categories (first 5): {user_categories[:5]}")

# ============================================================
# 12. TYPE CASTING
# ============================================================
print("\n12. TYPE CASTING")
print("-" * 40)

# Cast to string
query = select(cast(User.id, String).label('id_as_string'))
id_strings = session.execute(query).all()
print(f"IDs as strings (first 3): {id_strings[:3]}")

# Cast to integer (if applicable)
query = select(cast(User.first_name, String).label('name_as_string'))
name_strings = session.execute(query).all()
print(f"Names as strings (first 3): {name_strings[:3]}")

# ============================================================
# 13. SUBQUERIES
# ============================================================
print("\n13. SUBQUERIES")
print("-" * 40)

# Scalar subquery
subquery = select(func.count(User.id)).where(User.first_name == "John")
query = select(User).where(User.id > subquery.scalar_subquery())
users_after_john_count = session.execute(query).scalars().all()
print(f"Users after John count: {len(users_after_john_count)}")

# EXISTS subquery
subquery = select(Address.id).where(Address.user_id == User.id)
query = select(User).where(subquery.exists())
users_with_addresses = session.execute(query).scalars().all()
print(f"Users with addresses: {len(users_with_addresses)}")

# NOT EXISTS subquery
query = select(User).where(~subquery.exists())
users_without_addresses = session.execute(query).scalars().all()
print(f"Users without addresses: {len(users_without_addresses)}")

# ============================================================
# 14. WINDOW FUNCTIONS
# ============================================================
print("\n14. WINDOW FUNCTIONS")
print("-" * 40)

from sqlalchemy import over

# ROW_NUMBER
query = (
    select(
        User.first_name,
        User.last_name,
        func.row_number().over(order_by=User.first_name).label('row_num')
    )
)
row_numbers = session.execute(query).all()
print(f"Row numbers (first 5): {row_numbers[:5]}")

# RANK
query = (
    select(
        User.first_name,
        func.rank().over(order_by=User.first_name).label('rank')
    )
)
ranks = session.execute(query).all()
print(f"Ranks (first 5): {ranks[:5]}")

# DENSE_RANK
query = (
    select(
        User.first_name,
        func.dense_rank().over(order_by=User.first_name).label('dense_rank')
    )
)
dense_ranks = session.execute(query).all()
print(f"Dense ranks (first 5): {dense_ranks[:5]}")

# ============================================================
# 15. EAGER LOADING
# ============================================================
print("\n15. EAGER LOADING")
print("-" * 40)

# selectinload (for collections)

# Query to get addresses with their associated users
query = select(Address).options(selectinload(Address.user))
addresses_with_users = session.execute(query).scalars().all()

print("Addresses with their associated users:")
for address in addresses_with_users:
    print(f"Address ID: {address.id}")
    print(f"City: {address.city}")
    print(f"User: {address.user}")

# Query to get users with their associated addresses 
print("Users with their addresses:")
query_users = select(User).options(selectinload(User.addresses))
users_with_addresses = session.execute(query_users).scalars().all()
for user in users_with_addresses:
    print(f"\nUser: {user}")
    if user.addresses:
        print("  Addresses:")
        for address in user.addresses:
            print(f"{address.id}, {address.city}")
    else:
        print("No addresses")

# joinedload (for single relationships)
query = select(User).options(joinedload(User.preference))
users_with_preferences = session.execute(query).scalars().all()
print(f"Users with eagerly loaded preferences: {len(users_with_preferences)}")

# subqueryload (alternative to selectinload)
query = select(User).options(subqueryload(User.roles))
users_with_roles = session.execute(query).scalars().all()
print(f"Users with eagerly loaded roles: {len(users_with_roles)}")

# ============================================================
# 16. UNION AND SET OPERATIONS
# ============================================================
print("\n16. UNION AND SET OPERATIONS")
print("-" * 40)

from sqlalchemy import union, union_all, intersect, except_

# UNION
query1 = select(User.first_name).where(User.first_name.like("J%"))
query2 = select(User.last_name).where(User.last_name.like("D%"))
union_query = union(query1, query2)
union_results = session.execute(union_query).all()
print(f"UNION results (first 5): {union_results[:5]}")

# UNION ALL
union_all_query = union_all(query1, query2)
union_all_results = session.execute(union_all_query).all()
print(f"UNION ALL results (first 5): {union_all_results[:5]}")

# ============================================================
# 17. ADVANCED FILTERING
# ============================================================
print("\n17. ADVANCED FILTERING")
print("-" * 40)

# Multiple AND/OR combinations
query = select(User).where(
    and_(
        or_(
            User.first_name == "John",
            User.first_name == "Jane"
        ),
        User.email.contains("gmail"),
        User.id > 0
    )
)
complex_filtered = session.execute(query).scalars().all()
print(f"Complex filtered users: {len(complex_filtered)}")

# Nested conditions
query = select(User).where(
    or_(
        and_(User.first_name == "John", User.last_name == "Doe"),
        and_(User.first_name == "Jane", User.last_name == "Smith")
    )
)
nested_filtered = session.execute(query).scalars().all()
print(f"Nested filtered users: {len(nested_filtered)}")

# ============================================================
# 18. TEXT SQL
# ============================================================
print("\n18. TEXT SQL")
print("-" * 40)

from sqlalchemy import text

# Raw SQL with text()
query = text("SELECT first_name, last_name FROM users WHERE first_name = :name")
raw_results = session.execute(query, {"name": "John"}).all()
print(f"Raw SQL results: {raw_results}")

# Text with parameters
query = text("SELECT COUNT(*) as count FROM users WHERE first_name LIKE :pattern")
count_result = session.execute(query, {"pattern": "J%"}).scalar()
print(f"Raw SQL count: {count_result}")

# ============================================================
# 19. COMPLEX AGGREGATIONS
# ============================================================
print("\n19. COMPLEX AGGREGATIONS")
print("-" * 40)

# Multiple aggregations in one query
query = (
    select(
        func.count(User.id).label('total_users'),
        func.count(distinct(User.first_name)).label('unique_names'),
        func.max(User.id).label('max_id'),
        func.min(User.id).label('min_id')
    )
)
stats = session.execute(query).first()
print(f"User statistics: {stats}")

# Conditional aggregation
query = (
    select(
        func.count(case((User.first_name == "John", 1))).label('john_count'),
        func.count(case((User.first_name == "Jane", 1))).label('jane_count'),
        func.count(case((User.first_name.not_in(["John", "Jane"]), 1))).label('other_count')
    )
)
conditional_stats = session.execute(query).first()
print(f"Conditional statistics: {conditional_stats}")

# ============================================================
# 20. PERFORMANCE OPTIMIZATIONS
# ============================================================
print("\n20. PERFORMANCE OPTIMIZATIONS")
print("-" * 40)

# Using DISTINCT
query = select(distinct(User.first_name))
unique_first_names = session.execute(query).all()
print(f"Unique first names: {len(unique_first_names)}")

# Using LIMIT for testing
query = select(User).limit(1)
test_user = session.execute(query).scalar()
print(f"Test user: {test_user.first_name if test_user else 'None'}")

# Using specific columns instead of all
query = select(User.id, User.first_name, User.email)
specific_columns = session.execute(query).all()
print(f"Specific columns (first 3): {specific_columns[:3]}")

print("\n" + "=" * 70)
print("SQLALCHEMY 2.0 QUERY METHODS COMPLETE!")
print("=" * 70)
