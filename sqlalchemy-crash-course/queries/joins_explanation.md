# SQLAlchemy Joins - Complete Learning Guide

This document explains all the join examples in `queries/joins.py` from simple to complex.

## 1. SIMPLE INNER JOIN
```python
query = select(User).join(User.addresses)
```
**What it does:** Gets all users who have addresses
**SQL Generated:** `SELECT users.* FROM users JOIN addresses ON users.id = addresses.user_id`
**Use case:** When you only want records that have matching data in both tables

## 2. LEFT JOIN (OUTER JOIN)
```python
query = select(User).outerjoin(User.addresses)
```
**What it does:** Gets all users, including those without addresses
**SQL Generated:** `SELECT users.* FROM users LEFT OUTER JOIN addresses ON users.id = addresses.user_id`
**Use case:** When you want all records from the left table, even if there's no match in the right table

## 3. JOIN WITH FILTERING
```python
query = select(User).join(User.addresses).where(Address.city == "London")
```
**What it does:** Gets users who have addresses in London
**SQL Generated:** `SELECT users.* FROM users JOIN addresses ON users.id = addresses.user_id WHERE addresses.city = 'London'`
**Use case:** Combining joins with WHERE conditions to filter results

## 4. MULTIPLE JOINS
```python
query = select(User).join(User.addresses).join(User.roles)
```
**What it does:** Gets users who have both addresses and roles
**SQL Generated:** Multiple JOIN clauses connecting users to addresses and roles
**Use case:** When you need data from multiple related tables

## 5. JOIN WITH MULTIPLE CONDITIONS
```python
query = (
    select(User)
    .join(User.roles)
    .join(User.addresses)
    .where(and_(
        Role.slug == "admin",
        Address.city.in_(["London", "New York", "Lahore"])
    ))
)
```
**What it does:** Gets admin users who have addresses in specific cities
**Use case:** Complex filtering with multiple conditions using `and_()` and `in_()`

## 6. SELF JOIN EXAMPLE
```python
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
    .having(func.count(User.id) > 1)
)
```
**What it does:** Finds users with duplicate first names
**Use case:** Grouping and aggregation with HAVING clause

## 7. COMPLEX JOIN WITH SUBQUERY
```python
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
```
**What it does:** Gets users who have addresses in cities that have multiple addresses
**Use case:** Using subqueries to create complex filtering conditions

## 8. CROSS JOIN EXAMPLE
```python
query = select(User.first_name, Role.name).select_from(User).join(User.roles)
```
**What it does:** Gets all possible user-role combinations
**Use case:** Creating combinations of data from different tables

## 9. ADVANCED: JOIN WITH AGGREGATION AND ORDERING
```python
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
```
**What it does:** Gets users with their address count, ordered by address count
**Use case:** Aggregation with grouping and ordering

## 10. COMPLEX: MULTIPLE JOINS WITH CONDITIONAL LOGIC
```python
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
```
**What it does:** Gets users meeting complex criteria with multiple OR conditions
**Use case:** Complex business logic with multiple conditions and pattern matching

## 11. ADVANCED: JOIN WITH WINDOW FUNCTIONS
```python
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
```
**What it does:** Gets users with their address count and ranking
**Use case:** Creating rankings and ordered lists with aggregation

## 12. ULTRA COMPLEX: MULTIPLE SUBQUERIES AND JOINS
```python
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
```
**What it does:** Finds users who share the same role as users with London addresses
**Use case:** Complex nested subqueries for advanced data analysis

## Key SQLAlchemy 2.0 Join Concepts:

### Join Types:
- **`.join()`** - INNER JOIN
- **`.outerjoin()`** - LEFT OUTER JOIN
- **`.cross_join()`** - CROSS JOIN (not directly supported in SQLAlchemy 2.0)

### Common Methods:
- **`.where()`** - Filter conditions
- **`.and_()`** - AND conditions
- **`.or_()`** - OR conditions
- **`.in_()`** - IN conditions
- **`.like()`** - Pattern matching
- **`.distinct()`** - Remove duplicates
- **`.group_by()`** - Group results
- **`.having()`** - Filter grouped results
- **`.order_by()`** - Sort results
- **`.limit()`** - Limit results
- **`.offset()`** - Skip results

### Subquery Types:
- **`.scalar_subquery()`** - Single value subquery
- **`.subquery()`** - Table subquery

### Aggregation Functions:
- **`func.count()`** - Count records
- **`func.avg()`** - Average
- **`func.sum()`** - Sum
- **`func.max()`** - Maximum
- **`func.min()`** - Minimum

## Best Practices:

1. **Separate query construction from execution** for better readability
2. **Use descriptive variable names** for queries
3. **Add comments** explaining complex logic
4. **Use `.distinct()`** when joins might create duplicates
5. **Consider performance** when using multiple joins
6. **Use appropriate join types** based on your data requirements
7. **Test queries** with different data scenarios

## Common Patterns:

### Pattern 1: Basic Join with Filter
```python
query = select(User).join(User.addresses).where(Address.city == "London")
```

### Pattern 2: Multiple Joins
```python
query = select(User).join(User.addresses).join(User.roles)
```

### Pattern 3: Aggregation with Join
```python
query = (
    select(User.first_name, func.count(Address.id))
    .outerjoin(User.addresses)
    .group_by(User.first_name)
)
```

### Pattern 4: Subquery in WHERE
```python
subquery = select(Address.city).where(Address.city.like("L%"))
query = select(User).join(User.addresses).where(Address.city.in_(subquery))
```

This comprehensive guide covers all the essential join patterns you'll need for SQLAlchemy 2.0 development!
