# SQLAlchemy 2.0 Query Methods - Complete Reference Guide

This comprehensive guide covers all the query methods available in SQLAlchemy 2.0, from basic to advanced operations.

## Table of Contents
1. [Basic Select Methods](#1-basic-select-methods)
2. [Filtering Methods](#2-filtering-methods)
3. [Comparison Operators](#3-comparison-operators)
4. [String Operations](#4-string-operations)
5. [IN and NOT IN Operations](#5-in-and-not-in-operations)
6. [NULL Operations](#6-null-operations)
7. [Ordering Methods](#7-ordering-methods)
8. [Limit and Offset](#8-limit-and-offset)
9. [Aggregation Functions](#9-aggregation-functions)
10. [Group By and Having](#10-group-by-and-having)
11. [Case Statements](#11-case-statements)
12. [Type Casting](#12-type-casting)
13. [Subqueries](#13-subqueries)
14. [Window Functions](#14-window-functions)
15. [Eager Loading](#15-eager-loading)
16. [Union and Set Operations](#16-union-and-set-operations)
17. [Advanced Filtering](#17-advanced-filtering)
18. [Text SQL](#18-text-sql)
19. [Complex Aggregations](#19-complex-aggregations)
20. [Performance Optimizations](#20-performance-optimizations)

---

## 1. Basic Select Methods

### Basic Select
```python
# Select all columns from a table
query = select(User)
all_users = session.execute(query).scalars().all()
```

### Select Specific Columns
```python
# Select only specific columns
query = select(User.first_name, User.last_name, User.email)
user_data = session.execute(query).all()
```

### Select with Alias
```python
# Use table aliases
from sqlalchemy import alias
user_alias = alias(User, name="u")
query = select(user_alias.c.first_name, user_alias.c.last_name)
```

**Use Cases:**
- Basic data retrieval
- Performance optimization (selecting only needed columns)
- Complex queries with table aliases

---

## 2. Filtering Methods

### Basic WHERE Clause
```python
query = select(User).where(User.first_name == "John")
```

### Multiple Conditions with AND
```python
query = select(User).where(
    and_(
        User.first_name == "John",
        User.last_name == "Doe"
    )
)
```

### Multiple Conditions with OR
```python
query = select(User).where(
    or_(
        User.first_name == "John",
        User.first_name == "Jane"
    )
)
```

### NOT Condition
```python
query = select(User).where(not_(User.first_name == "John"))
```

**Use Cases:**
- Data filtering
- Complex conditional logic
- Data validation queries

---

## 3. Comparison Operators

### Equal and Not Equal
```python
# Equal
query = select(User).where(User.first_name == "John")

# Not equal
query = select(User).where(User.first_name != "John")
```

### Numeric Comparisons
```python
# Greater than
query = select(User).where(User.id > 5)

# Less than or equal
query = select(User).where(User.id <= 5)

# Between
query = select(User).where(User.id.between(1, 5))
```

**Use Cases:**
- Range queries
- Numeric filtering
- ID-based operations

---

## 4. String Operations

### Pattern Matching
```python
# LIKE with wildcards
query = select(User).where(User.first_name.like("J%"))

# ILIKE (case insensitive)
query = select(User).where(User.first_name.ilike("j%"))

# Contains
query = select(User).where(User.email.contains("gmail"))

# Starts with
query = select(User).where(User.first_name.startswith("J"))

# Ends with
query = select(User).where(User.email.endswith(".com"))
```

**Use Cases:**
- Text search
- Email filtering
- Name pattern matching

---

## 5. IN and NOT IN Operations

### IN Operator
```python
# Simple IN
query = select(User).where(User.first_name.in_(["John", "Jane", "Bob"]))

# IN with subquery
subquery = select(Address.user_id).where(Address.city == "London")
query = select(User).where(User.id.in_(subquery))
```

### NOT IN Operator
```python
query = select(User).where(User.first_name.not_in(["John", "Jane"]))
```

**Use Cases:**
- Multiple value filtering
- Subquery-based filtering
- Exclusion queries

---

## 6. NULL Operations

### IS NULL and IS NOT NULL
```python
# IS NULL
query = select(User).where(User.first_name.is_(None))

# IS NOT NULL
query = select(User).where(User.first_name.is_not(None))
```

**Use Cases:**
- Data validation
- Missing data queries
- Data quality checks

---

## 7. Ordering Methods

### Basic Ordering
```python
# Ascending order
query = select(User).order_by(User.first_name)

# Descending order
query = select(User).order_by(desc(User.first_name))

# Multiple columns
query = select(User).order_by(User.first_name, User.last_name)
```

**Use Cases:**
- Data presentation
- Ranking queries
- Sorted lists

---

## 8. Limit and Offset

### Pagination
```python
# LIMIT
query = select(User).limit(3)

# OFFSET
query = select(User).offset(3)

# Pagination (LIMIT + OFFSET)
query = select(User).limit(2).offset(2)
```

**Use Cases:**
- Pagination
- Performance optimization
- Large dataset handling

---

## 9. Aggregation Functions

### Basic Aggregations
```python
# COUNT
query = select(func.count(User.id))

# COUNT DISTINCT
query = select(func.count(distinct(User.first_name)))

# MAX, MIN, AVG, SUM
query = select(func.max(User.id))
query = select(func.min(User.id))
query = select(func.avg(User.id))
query = select(func.sum(User.id))
```

**Use Cases:**
- Statistics
- Data analysis
- Reporting queries

---

## 10. Group By and Having

### Group By
```python
# Simple GROUP BY
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
)

# GROUP BY with HAVING
query = (
    select(User.first_name, func.count(User.id).label('count'))
    .group_by(User.first_name)
    .having(func.count(User.id) > 1)
)

# Multiple GROUP BY columns
query = (
    select(User.first_name, User.last_name, func.count(User.id).label('count'))
    .group_by(User.first_name, User.last_name)
)
```

**Use Cases:**
- Data grouping
- Duplicate detection
- Statistical analysis

---

## 11. Case Statements

### Simple CASE
```python
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
```

### Complex CASE
```python
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
```

**Use Cases:**
- Conditional logic
- Data categorization
- Business rule implementation

---

## 12. Type Casting

### Cast Operations
```python
# Cast to string
query = select(cast(User.id, String).label('id_as_string'))

# Cast to integer
query = select(cast(User.first_name, String).label('name_as_string'))
```

**Use Cases:**
- Data type conversion
- Formatting
- Compatibility

---

## 13. Subqueries

### Scalar Subquery
```python
subquery = select(func.count(User.id)).where(User.first_name == "John")
query = select(User).where(User.id > subquery.scalar_subquery())
```

### EXISTS Subquery
```python
subquery = select(Address.id).where(Address.user_id == User.id)
query = select(User).where(subquery.exists())

# NOT EXISTS
query = select(User).where(~subquery.exists())
```

**Use Cases:**
- Complex filtering
- Performance optimization
- Related data queries

---

## 14. Window Functions

### Ranking Functions
```python
from sqlalchemy import over

# ROW_NUMBER
query = (
    select(
        User.first_name,
        User.last_name,
        func.row_number().over(order_by=User.first_name).label('row_num')
    )
)

# RANK
query = (
    select(
        User.first_name,
        func.rank().over(order_by=User.first_name).label('rank')
    )
)

# DENSE_RANK
query = (
    select(
        User.first_name,
        func.dense_rank().over(order_by=User.first_name).label('dense_rank')
    )
)
```

**Use Cases:**
- Ranking
- Analytics
- Data ordering

---

## 15. Eager Loading

### Loading Strategies
```python
# selectinload (for collections)
query = select(User).options(selectinload(User.addresses))

# joinedload (for single relationships)
query = select(User).options(joinedload(User.preference))

# subqueryload (alternative to selectinload)
query = select(User).options(subqueryload(User.roles))
```

**Use Cases:**
- Performance optimization
- N+1 query prevention
- Related data loading

---

## 16. Union and Set Operations

### Set Operations
```python
from sqlalchemy import union, union_all, intersect, except_

# UNION
query1 = select(User.first_name).where(User.first_name.like("J%"))
query2 = select(User.last_name).where(User.last_name.like("D%"))
union_query = union(query1, query2)

# UNION ALL
union_all_query = union_all(query1, query2)
```

**Use Cases:**
- Data combination
- Complex reporting
- Multiple source queries

---

## 17. Advanced Filtering

### Complex Conditions
```python
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

# Nested conditions
query = select(User).where(
    or_(
        and_(User.first_name == "John", User.last_name == "Doe"),
        and_(User.first_name == "Jane", User.last_name == "Smith")
    )
)
```

**Use Cases:**
- Complex business logic
- Multi-criteria filtering
- Advanced search

---

## 18. Text SQL

### Raw SQL
```python
from sqlalchemy import text

# Raw SQL with parameters
query = text("SELECT first_name, last_name FROM users WHERE first_name = :name")
raw_results = session.execute(query, {"name": "John"}).all()

# Text with aggregation
query = text("SELECT COUNT(*) as count FROM users WHERE first_name LIKE :pattern")
count_result = session.execute(query, {"pattern": "J%"}).scalar()
```

**Use Cases:**
- Complex SQL not expressible in ORM
- Legacy SQL integration
- Database-specific features

---

## 19. Complex Aggregations

### Multiple Aggregations
```python
# Multiple aggregations in one query
query = (
    select(
        func.count(User.id).label('total_users'),
        func.count(distinct(User.first_name)).label('unique_names'),
        func.max(User.id).label('max_id'),
        func.min(User.id).label('min_id')
    )
)

# Conditional aggregation
query = (
    select(
        func.count(case((User.first_name == "John", 1))).label('john_count'),
        func.count(case((User.first_name == "Jane", 1))).label('jane_count'),
        func.count(case((User.first_name.not_in(["John", "Jane"]), 1))).label('other_count')
    )
)
```

**Use Cases:**
- Complex reporting
- Data analysis
- Business intelligence

---

## 20. Performance Optimizations

### Optimization Techniques
```python
# Using DISTINCT
query = select(distinct(User.first_name))

# Using LIMIT for testing
query = select(User).limit(1)

# Using specific columns instead of all
query = select(User.id, User.first_name, User.email)
```

**Use Cases:**
- Performance improvement
- Memory optimization
- Query efficiency

---

## Best Practices

### 1. Query Construction
- Separate query building from execution
- Use descriptive variable names
- Add comments for complex logic

### 2. Performance
- Use appropriate indexes
- Limit result sets when possible
- Use eager loading for related data
- Avoid N+1 queries

### 3. Readability
- Use consistent formatting
- Break complex queries into parts
- Use meaningful aliases

### 4. Security
- Use parameterized queries
- Validate input data
- Avoid SQL injection

### 5. Maintenance
- Document complex queries
- Use version control
- Test queries with different data scenarios

## Common Patterns

### Pattern 1: Basic CRUD Operations
```python
# Create
user = User(first_name="John", last_name="Doe")
session.add(user)
session.commit()

# Read
user = session.execute(select(User).where(User.id == 1)).scalar()

# Update
user.first_name = "Jane"
session.commit()

# Delete
session.delete(user)
session.commit()
```

### Pattern 2: Pagination
```python
def get_paginated_users(page: int, per_page: int):
    offset = (page - 1) * per_page
    query = select(User).limit(per_page).offset(offset)
    return session.execute(query).scalars().all()
```

### Pattern 3: Search with Multiple Criteria
```python
def search_users(name: str = None, email: str = None, city: str = None):
    query = select(User)
    
    if name:
        query = query.where(User.first_name.contains(name))
    if email:
        query = query.where(User.email.contains(email))
    if city:
        query = query.join(User.addresses).where(Address.city == city)
    
    return session.execute(query).scalars().all()
```

### Pattern 4: Aggregation with Grouping
```python
def get_user_statistics():
    query = (
        select(
            User.first_name,
            func.count(Address.id).label('address_count'),
            func.count(Role.id).label('role_count')
        )
        .outerjoin(User.addresses)
        .outerjoin(User.roles)
        .group_by(User.first_name)
        .order_by(desc(func.count(Address.id)))
    )
    return session.execute(query).all()
```

This comprehensive guide covers all the essential SQLAlchemy 2.0 query methods you'll need for database operations!
