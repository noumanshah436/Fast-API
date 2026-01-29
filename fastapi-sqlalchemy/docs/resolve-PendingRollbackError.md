Ah! This error is **very common when working with async SQLAlchemy and unique constraints**. Let’s go **carefully step by step**.

---

## 1️⃣ What the error means

```text
PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush.
Original exception: UniqueViolationError: duplicate key value violates unique constraint "users_email_key"
Key (email)=(nouman@gmail.com) already exists.
```

* You tried to insert a new user with **email `nouman@gmail.com`**
* Your `User` model has:

```python
email = Column(String, unique=True, nullable=False)
```

* PostgreSQL **does not allow duplicate values** in a `UNIQUE` column → triggers **IntegrityError**
* SQLAlchemy marks the session as **“broken”** → any further operations **fail with `PendingRollbackError`**

---

## 2️⃣ Why `PendingRollbackError` happens

* In async SQLAlchemy, when a flush/commit fails:

  ```python
  await session.commit()
  ```

  the **whole transaction is rolled back automatically**, but the **Session is still “dirty”**.
* You **cannot continue using the session** until you explicitly **rollback**:

```python
await session.rollback()
```

Otherwise, you get:

```text
PendingRollbackError
```

---

## 3️⃣ Correct pattern to handle unique constraint inserts

### Step 1: Check if user exists before insert

```python
from sqlalchemy import select

result = await session.execute(select(User).where(User.email == "nouman@gmail.com"))
existing_user = result.scalar_one_or_none()

if existing_user:
    print("User already exists!")
else:
    new_user = User(name="Nouman042", email="nouman@gmail.com")
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    print(new_user.id)
```

---

### Step 2: Handle exception and rollback

```python
from sqlalchemy.exc import IntegrityError

new_user = User(name="Nouman042", email="nouman@gmail.com")
session.add(new_user)

try:
    await session.commit()
except IntegrityError:
    await session.rollback()  # important!
    print("User already exists or other integrity error")
```

* Always **rollback** after an error → session can be used again
* This works for **async sessions too**

---

## 4️⃣ Key points to remember

| Problem                | Solution                                           |
| ---------------------- | -------------------------------------------------- |
| `PendingRollbackError` | `await session.rollback()` after exception         |
| Unique key violation   | Either **check first** or **catch IntegrityError** |
| Async session commit   | Always `await session.commit()`                    |

---

### ✅ Recommended “upsert” pattern (insert-or-ignore)

In PostgreSQL, you can also do **insert only if not exists**:

```python
from sqlalchemy.dialects.postgresql import insert

stmt = insert(User).values(name="Nouman042", email="nouman@gmail.com").on_conflict_do_nothing()
await session.execute(stmt)
await session.commit()
```

* Avoids manual check
* Very efficient for bulk inserts

---

So in short:

1. **Session is broken after a unique violation** → rollback needed
2. **Check for duplicates or use `on_conflict_do_nothing()`**
3. **Always `await` async operations**

---

If you want, I can write a **full async CRUD “safe insert” function for User** that **handles duplicates and rollbacks cleanly** in your FastAPI setup.

Do you want me to do that?
