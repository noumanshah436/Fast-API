Below is a **deep, structured explanation** of *Joined Table Inheritance in SQLAlchemy* with simple intuition, diagrams, SQL examples, and practical implications — tailored for someone already working with FastAPI + SQLAlchemy like you.

---

# ✅ What is **Joined Table Inheritance**?

Joined Table Inheritance means:

> 👉 **Each class in your inheritance hierarchy has its OWN table in the database.**
> 👉 Objects are reconstructed using SQL **JOINs** across those tables.

This is the most *normalized* form of inheritance mapping.

---

# 🔹 Big Picture (Intuition First)

Imagine you have employees:

* Some are **generic employees**
* Some are **Engineers**
* Some are **Managers**

Conceptually:

```
Employee   → common attributes
   |
   |---- Engineer → extra attributes
   |
   |---- Manager  → extra attributes
```

### Tables in Joined Inheritance:

You will get **three tables**, not one:

| Table    | Columns           |
| -------- | ----------------- |
| employee | id, name, type    |
| engineer | id, engineer_name |
| manager  | id, manager_name  |

🔹 Notice:

* `engineer.id` and `manager.id` are **FK to employee.id**
* Every Engineer and Manager is *also* an Employee

This is why it’s called **joined** inheritance — SQLAlchemy must JOIN tables to load subclasses.

---

# 🔹 The Discriminator (`polymorphic_on`)

You define this in the base class:

```python
class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]   # 👈 DISCRIMINATOR COLUMN

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }
```

### What does `type` do?

It tells SQLAlchemy:

> “When you load a row, look at this column to decide which Python class to create.”

Example rows in `employee` table:

| id | name  | type     |
| -- | ----- | -------- |
| 1  | Ali   | employee |
| 2  | Sara  | engineer |
| 3  | Ahmed | manager  |

When SQLAlchemy sees:

* `type = "engineer"` → create `Engineer` object
* `type = "manager"` → create `Manager` object
* `type = "employee"` → create `Employee` object

This is **polymorphism in ORM form.**

---

# 🔹 Subclasses Tables

### Engineer table

```python
class Engineer(Employee):
    __tablename__ = "engineer"

    id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), primary_key=True
    )
    engineer_name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "engineer",
    }
```

Database will look like:

| id | engineer_name |
| -- | ------------- |
| 2  | Backend Lead  |

And in `employee` table:

| id | name | type     |
| -- | ---- | -------- |
| 2  | Sara | engineer |

So one Engineer lives in **two tables**.

---

# 🔹 What SQL does SQLAlchemy generate?

If you query:

```python
session.query(Employee).all()
```

SQL will be roughly like:

```sql
SELECT *
FROM employee
LEFT JOIN engineer ON employee.id = engineer.id
LEFT JOIN manager ON employee.id = manager.id;
```

So:

* One row in Python = data from multiple tables
* But identity is based **only on employee.id**

---

# 🔹 VERY IMPORTANT POINT — Primary Keys

SQLAlchemy treats:

> 👉 **Only `employee.id` as the real identity of the object.**

Even though `engineer.id` exists, SQLAlchemy does NOT treat it as a separate identity.

So:

* Engineer(2)
* Employee(2)

Both refer to the **same person**, just different layers of data.

---

# 🔹 Creating Objects

If you create:

```python
eng = Engineer(name="Sara", engineer_name="Backend Lead")
session.add(eng)
session.commit()
```

SQLAlchemy inserts:

### 1️⃣ Into employee:

| id | name | type     |
| -- | ---- | -------- |
| 2  | Sara | engineer |

### 2️⃣ Into engineer:

| id | engineer_name |
| -- | ------------- |
| 2  | Backend Lead  |

You **never manually set `type`** — SQLAlchemy sets it automatically using `polymorphic_identity`.

---

# 🔹 Relationships with Joined Inheritance

Example 1 — FK is on **Employee**

```python
class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    employees: Mapped[List[Employee]] = relationship(back_populates="company")
```

```python
class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "employee",
    }
```

Now:

```python
company.employees
```

can contain:

* Employee objects
* Engineer objects
* Manager objects

All mixed together ✅

---

# 🔹 Example 2 — FK is on Subclass (Manager)

If `company_id` is on **manager table**, relationship is set there:

```python
class Manager(Employee):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), primary_key=True
    )
    manager_name: Mapped[str]

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped[Company] = relationship(back_populates="managers")

    __mapper_args__ = {"polymorphic_identity": "manager"}
```

Then:

```python
company.managers
```

will load **only managers**, joining `employee + manager` tables automatically.

---

# ✅ Advantages of Joined Table Inheritance

| Benefit           | Explanation                      |
| ----------------- | -------------------------------- |
| Normalized DB     | No duplicate columns             |
| Clean schema      | Each subclass has its own table  |
| Flexible          | You can add new subclasses later |
| Real polymorphism | Works naturally in Python        |

---

# ⚠️ Disadvantages

| Issue            | Explanation                          |
| ---------------- | ------------------------------------ |
| More JOINs       | Slower than single-table inheritance |
| More complex SQL | Harder to debug                      |
| More tables      | More migrations                      |

---

# 🔹 When should YOU (Nouman) use this?

Since you're working with **FastAPI + SQLAlchemy**, use joined inheritance when:

* You have **real domain inheritance**, e.g.

  * User → Admin, Doctor, Patient
  * Document → Invoice, Report, Prescription
  * Notification → Email, Slack, SMS

Do **NOT** use it if subclasses only differ by 1–2 fields — then Single Table Inheritance is simpler.

---

# If you want, I can:

* draw a clean database diagram 🗺️
* show real SQL logs in FastAPI 🔍
* compare **Joined vs Single vs Concrete** inheritance
* implement this in your existing FastAPI project

Just tell me 👍
