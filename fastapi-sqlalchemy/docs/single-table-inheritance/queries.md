Below is a **practical CRUD + querying guide** for **your exact STI models** (`CompanySTI`, `EmployeeSTI`, `ManagerSTI`, `EngineerSTI`) in **FastAPI + SQLAlchemy 2.0 (async style)** — with:

* multiple **ways to insert data**
* real **STI-aware queries**
* **eager loading**
* common **optimizations**
* pitfalls to avoid

You should be able to copy-paste most of this directly into your project.

---

# =========================================

# 0️⃣ ASSUMED SESSION STYLE (your stack)

# =========================================

I’ll assume you are using something like:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
```

And dependency in FastAPI:

```python
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
```

---

# =========================================

# 1️⃣ CREATE OPERATIONS (Different Ways)

# =========================================

## ✅ **A) Create Company first (recommended pattern)**

```python
async def create_company(session: AsyncSession):
    company = CompanySTI(name="Tech Corp")

    session.add(company)
    await session.commit()
    await session.refresh(company)

    return company
```

---

## ✅ **B) Create Manager (basic way)**

```python
async def create_manager(session: AsyncSession, company_id: int):
    manager = ManagerSTI(
        name="Ali",
        manager_data="HR Lead",
        company_id=company_id,
    )

    session.add(manager)
    await session.commit()
    await session.refresh(manager)

    return manager
```

👉 This will INSERT into **employee_sti** with:

```
type = "manager_sti"
```

---

## ✅ **C) Create Engineer**

```python
async def create_engineer(session: AsyncSession, company_id: int):
    engineer = EngineerSTI(
        name="Ahmed",
        engineer_info="Backend expert",
        company_id=company_id,
    )

    session.add(engineer)
    await session.commit()
    await session.refresh(engineer)

    return engineer
```

---

## ✅ **D) Create multiple employees at once (bulk safe way)**

```python
async def bulk_create_employees(session: AsyncSession, company_id: int):
    employees = [
        ManagerSTI(
            name="Ali",
            manager_data="HR Lead",
            company_id=company_id,
        ),
        EngineerSTI(
            name="Ahmed",
            engineer_info="Backend expert",
            company_id=company_id,
        ),
    ]

    session.add_all(employees)
    await session.commit()

    return employees
```

---

## ⚠️ **Avoid raw bulk_insert for STI**

❌ Don’t do this with STI:

```python
await session.execute(
    insert(EmployeeSTI).values(name="X", type="manager_sti")
)
```

Why?
You bypass polymorphic mapping and relationships.

Use **ORM objects instead.**

---

# =========================================

# 2️⃣ READ QUERIES (STI-AWARE)

# =========================================

## ✅ **Get all employees (mixed types)**

```python
async def get_all_employees(session: AsyncSession):
    result = await session.scalars(
        select(EmployeeSTI)
    )
    return result.all()
```

You will get a **mix of:**

* `EmployeeSTI`
* `ManagerSTI`
* `EngineerSTI`

SQL roughly:

```sql
SELECT * FROM employee_sti;
```

---

## ✅ **Get only Managers**

```python
async def get_managers(session: AsyncSession):
    result = await session.scalars(
        select(ManagerSTI)
    )
    return result.all()
```

SQL becomes roughly:

```sql
SELECT * FROM employee_sti
WHERE type = 'manager_sti';
```

---

## ✅ **Get only Engineers**

```python
async def get_engineers(session: AsyncSession):
    result = await session.scalars(
        select(EngineerSTI)
    )
    return result.all()
```

---

## ✅ **Get one employee by ID (polymorphic result)**

```python
async def get_employee(session: AsyncSession, emp_id: int):
    emp = await session.get(EmployeeSTI, emp_id)
    return emp
```

If the row has:

* `type = manager_sti` → you get `ManagerSTI`
* `type = engineer_sti` → you get `EngineerSTI`

---

## ✅ **Get company with all employees**

```python
async def get_company_with_emps(session: AsyncSession, company_id: int):
    company = await session.get(CompanySTI, company_id)
    return company
```

Access later:

```python
company.employees   # lazy load (not ideal)
```

---

# =========================================

# 3️⃣ EAGER LOADING (IMPORTANT OPTIMIZATION)

# =========================================

## 🚀 **Best practice: avoid N+1 queries**

Use `selectinload`.

### Get company + all employees in ONE query set

```python
from sqlalchemy.orm import selectinload

async def get_company_eager(session: AsyncSession, company_id: int):
    result = await session.scalars(
        select(CompanySTI)
        .options(selectinload(CompanySTI.employees))
        .where(CompanySTI.id == company_id)
    )

    return result.first()
```

Now:

```python
company = await get_company_eager(db, 1)

# NO extra DB queries here:
for emp in company.employees:
    print(emp.name, type(emp))
```

---

## 🚀 **Eager load only managers**

Add this relationship to `CompanySTI`:

```python
from sqlalchemy import and_

class CompanySTI(PostgresModel):
    __tablename__ = "company_sti"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    employees: Mapped[list["EmployeeSTI"]] = relationship(
        back_populates="company"
    )

    managers: Mapped[list["ManagerSTI"]] = relationship(
        primaryjoin=(
            and_(
                EmployeeSTI.company_id == id,
                EmployeeSTI.type == "manager_sti",
            )
        ),
        viewonly=True,
    )
```

Query:

```python
async def get_company_with_managers(session: AsyncSession, company_id: int):
    result = await session.scalars(
        select(CompanySTI)
        .options(selectinload(CompanySTI.managers))
        .where(CompanySTI.id == company_id)
    )
    return result.first()
```

---

# =========================================

# 4️⃣ UPDATE OPERATIONS

# =========================================

## Update Manager

```python
async def update_manager(session: AsyncSession, manager_id: int, new_data: str):
    manager = await session.get(ManagerSTI, manager_id)

    manager.manager_data = new_data
    await session.commit()
    await session.refresh(manager)

    return manager
```

---

## Change Engineer info

```python
async def update_engineer(session: AsyncSession, eng_id: int, new_info: str):
    engineer = await session.get(EngineerSTI, eng_id)

    engineer.engineer_info = new_info
    await session.commit()
    await session.refresh(engineer)

    return engineer
```

---

# =========================================

# 5️⃣ DELETE OPERATIONS

# =========================================

## Delete any employee (works for all types)

```python
async def delete_employee(session: AsyncSession, emp_id: int):
    emp = await session.get(EmployeeSTI, emp_id)
    await session.delete(emp)
    await session.commit()
```

This deletes from **employee_sti** only — which is correct for STI.

---

# =========================================

# 6️⃣ PERFORMANCE & OPTIMIZATION TIPS

# =========================================

## ✅ Add index on discriminator column (VERY IMPORTANT)

In Alembic:

```python
op.create_index(
    "ix_employee_sti_type",
    "employee_sti",
    ["type"]
)
```

Why?

Queries like:

```sql
WHERE type = 'manager_sti'
```

become **much faster**.

---

## ✅ Index on company_id

```python
op.create_index(
    "ix_employee_sti_company_id",
    "employee_sti",
    ["company_id"]
)
```

Speeds up:

```sql
WHERE company_id = 10
```

---

## ✅ Combined index (best)

```python
op.create_index(
    "ix_employee_sti_company_type",
    "employee_sti",
    ["company_id", "type"]
)
```

This is optimal for:

```sql
WHERE company_id = 1 AND type = 'manager_sti'
```

---

# =========================================

# 7️⃣ STI vs Joined (your real tradeoff)

# =========================================

| Feature      | Your STI (`employee_sti`) | Your Joined (`employee`) |
| ------------ | ------------------------- | ------------------------ |
| Tables       | 1                         | 3                        |
| Joins        | ❌ none                    | ✅ required               |
| Speed        | ⚡ faster                  | 🐌 slower                |
| Null columns | ✅ yes                     | ❌ no                     |
| Simplicity   | ✅ high                    | ❌ complex                |

Your use case (Employee → Manager/Engineer) is **good for STI.**

---

# =========================================

# 8️⃣ If you want next

# =========================================

I can now:

* build **FastAPI CRUD endpoints** for:

  * `/companies`
  * `/employees`
  * `/managers`
  * `/engineers`
* add **Pydantic schemas**
* or generate **Alembic migrations with indexes**

If you want, say:
👉 *“Give me full FastAPI CRUD for STI with Pydantic.”*
