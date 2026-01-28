Perfect 👍
Below is a **single inline async script** you can run in **IPython / Python shell / scratch file**.
No functions, no FastAPI dependencies — **just raw inline queries** using your `User` ↔ `Post` models.

Assumes:

* `AsyncSessionLocal` exists
* Models are `User`, `Post`
* PostgreSQL + async SQLAlchemy

---

# 🔹 Inline CRUD Script (Async SQLAlchemy)

```python
import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.config import AsyncSessionLocal
from src.database.models.user import User
from src.database.models.post import Post


async def main():
    # ----------------------------------
    # CREATE SESSION
    # ----------------------------------
    session = AsyncSessionLocal()

    try:
        # ----------------------------------
        # CREATE USER
        # ----------------------------------
        user = User(
            name="nouman",
            email="nouman@gmail.com",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        print("Created User:", user)

        # ----------------------------------
        # CREATE POSTS (via relationship)
        # ----------------------------------
        post1 = Post(
            title="First Post",
            description="This is my first post",
        )
        post2 = Post(
            title="Second Post",
            description="Another post",
        )

        user.posts.extend([post1, post2])
        await session.commit()

        print("Created Posts:", user.posts)

        # ----------------------------------
        # READ ALL USERS
        # ----------------------------------
        result = await session.execute(select(User))
        users = result.scalars().all()
        print("All Users:", users)

        # ----------------------------------
        # READ USER WITH POSTS
        # ----------------------------------
        result = await session.execute(
            select(User)
            .options(selectinload(User.posts))
            .where(User.id == user.id)
        )
        user_with_posts = result.scalar_one()
        print("User With Posts:", user_with_posts)
        print("Posts:", user_with_posts.posts)

        # ----------------------------------
        # READ POSTS BY USER
        # ----------------------------------
        result = await session.execute(
            select(Post).where(Post.user_id == user.id)
        )
        posts = result.scalars().all()
        print("Posts By User:", posts)

        # ----------------------------------
        # UPDATE USER
        # ----------------------------------
        user.name = "Nouman Updated"
        await session.commit()
        await session.refresh(user)
        print("Updated User:", user)

        # ----------------------------------
        # UPDATE POST
        # ----------------------------------
        post1.title = "Updated First Post"
        await session.commit()
        await session.refresh(post1)
        print("Updated Post:", post1)

        # ----------------------------------
        # DELETE ONE POST
        # ----------------------------------
        await session.delete(post2)
        await session.commit()
        print("Deleted Post 2")

        # ----------------------------------
        # VERIFY POSTS AFTER DELETE
        # ----------------------------------
        result = await session.execute(
            select(Post).where(Post.user_id == user.id)
        )
        remaining_posts = result.scalars().all()
        print("Remaining Posts:", remaining_posts)

        # ----------------------------------
        # DELETE USER (cascade deletes posts)
        # ----------------------------------
        await session.delete(user)
        await session.commit()
        print("Deleted User")

    finally:
        # ----------------------------------
        # CLOSE SESSION
        # ----------------------------------
        await session.close()


# Run inline
asyncio.run(main())
```

---

## 🔑 Important Notes

### ✔ Why this works cleanly

* No `async with`
* Single persistent session
* Manual `commit()` + `refresh()`
* Perfect for **learning, debugging, shell usage**

### ✔ Relationship behavior

* `user.posts.append(post)` automatically sets `post.user_id`
* Requires:

```python
posts = relationship(
    "Post",
    back_populates="user",
    cascade="all, delete-orphan",
)
```

---

## 🧠 Mental Model (remember forever)

```text
session.add()        → stage
await commit()       → persist
await refresh(obj)   → sync DB → Python
selectinload()       → eager relationship loading
```

---

If you want next:

* 🧩 Many-to-many inline script
* 🔥 JOIN queries inline
* 🧪 Transaction rollback demo
* 🧠 SQLAlchemy relationship cheatsheet
* ⚡ Convert this into FastAPI routes

Just tell me 👍
