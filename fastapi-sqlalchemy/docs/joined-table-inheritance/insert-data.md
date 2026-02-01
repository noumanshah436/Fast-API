Below I’ll give you **practical, runnable SQLAlchemy examples** for your exact models — with **multiple ways to INSERT data** and **multiple ways to QUERY data** (polymorphic + joins included).

I’ll assume you have a normal async or sync session like:

```python
from sqlalchemy.orm import Session

session: Session
```

(If you’re using `AsyncSession`, I can rewrite everything async for you — just tell me.)

---

# =========================

# ✅ PART 1 — INSERT DATA (Multiple Ways)

# =========================

## 🔹 **Way 1 — Create objects normally (recommended way)**

### Create company first

```python
company = Company(name="Tech Corp")
session.add(company)
await session.commit()
await session.refresh(company)
```

Now `company.id` is available.

---

## 🔹 **Way 2 — Create Engineer directly**

```python
eng = Engineer(
    name="Ali",
    engineer_name="Backend Engineer",
    company_id=company.id
)

session.add(eng)
await session.commit()
```

👉 What happens automatically in DB:

### `employee` table:

| id  | name | type     | company_id |
| --- | ---- | -------- | ---------- |
| 1   | Ali  | engineer | 1          |

### `engineer` table:

| id  | engineer_name    |
| --- | ---------------- |
| 1   | Backend Engineer |

You **never set `type` manually** — SQLAlchemy sets it to `"engineer"`.

---

## 🔹 **Way 3 — Create Manager directly**

```python
mgr = Manager(
    name="Sara",
    manager_name="Engineering Manager",
    company_id=company.id
)

session.add(mgr)
await session.commit()
```

DB will now have:

### `employee` table:

| id  | name | type    | company_id |
| --- | ---- | ------- | ---------- |
| 2   | Sara | manager | 1          |

### `manager` table:

| id  | manager_name        |
| --- | ------------------- |
| 2   | Engineering Manager |

---

## 🔹 **Way 4 — Create multiple employees at once (add_all)**

```python
e1 = Engineer(name="Hamza", engineer_name="ML Engineer", company_id=company.id)
e2 = Manager(name="Ayesha", manager_name="Product Manager", company_id=company.id)
e3 = Employee(name="Bilal", company_id=company.id)  # plain employee

session.add_all([e1, e2, e3])
await session.commit()
```

Now you have **3 different kinds of objects** saved correctly.

---

## 🔹 **Way 5 — Create via relationship (cleaner style)**

Instead of setting `company_id`, attach via relationship:

```python
eng = Engineer(
    name="Usman",
    engineer_name="DevOps Engineer",
    company=company   # <--- use relationship
)

session.add(eng)
await session.commit()
```

SQLAlchemy will automatically set `company_id` for you.

---

# =========================

# ✅ PART 2 — GET DATA (Multiple Ways)

# =========================

## 🔹 **Query 1 — Get ALL employees (polymorphic load)**

```python
result = await session.execute(select(Employee))
employees = result.scalars().all()
```

Result could be:

```
[
  Engineer(name="Ali"),
  Manager(name="Sara"),
  Employee(name="Bilal")
]
```

Even though you queried `Employee`, you get subclasses automatically.

---

## 🔹 **Query 2 — Get only Engineers**

```python
result = await session.execute(select(Engineer))
engineers = result.scalars().all()
```

or

```python
result = await session.execute(select(Employee).filter(Employee.type == "engineer"))
engineers = result.scalars().all()
```

Both work, but first is cleaner.

---

## 🔹 **Query 3 — Get only Managers**

```python
managers = (
    await session.execute(select(Manager))
).scalars().all()
```

---

## 🔹 **Query 4 — Get all employees of one company**

```python
stmt = (
    select(Company)
    .options(selectinload(Company.employees))
    .where(Company.name == "Tech Corp")
)

result = await session.execute(stmt)
company = result.scalars().first()

for emp in company.employees:
    print(emp, type(emp))
```

Example output:

```
Engineer('Ali') <class Engineer>
Manager('Sara') <class Manager>
Employee('Bilal') <class Employee>
```

---

## 🔹 **Query 5 — Join explicitly (SQL style)**

```python
from sqlalchemy import select

stmt = (
    select(Employee, Company)
    .join(Company, Employee.company_id == Company.id)
)

result = await session.execute(stmt)
rows = result.all()
```

Each row will be like:

```
(Employee(...), Company(...))
```

Usage:

```python
for emp, comp in rows:
    print(emp.name, "works at", comp.name)
```

---

## 🔹 **Query 6 — Get Engineers of a specific company**

---

## 🔹 **Query 7 — Load company + employees eagerly**

```python

from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_polymorphic
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

async def get_company(session: AsyncSession, company_name: str):
    # Load employees polymorphically
    EmployeePoly = with_polymorphic(Employee, [Engineer, Manager])

    result = await session.execute(
        select(Company)
        .options(selectinload(Company.employees.of_type(EmployeePoly)))
        .filter_by(name=company_name)
    )
    company = result.scalar_one_or_none()
    return company

company = await get_company(session, "Tech Corp")
print(company)
for emp in company.employees:
    print(emp, type(emp))
```