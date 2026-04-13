Great — these are **core concepts for performance + relationships in SQLAlchemy**, and honestly this is where most developers struggle in interviews.

Let’s break each one **clearly with examples + when to use** 👇

---

# 🧩 1. `relationship()`

This defines how two models are connected at the ORM level.

### Example (User → Posts)

```python
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")
```

### What happens?

* `user.posts` → list of posts
* `post.user` → single user

👉 `relationship()` does **NOT hit DB immediately** — loading depends on `lazy`

---

# 💤 2. `lazy='select' | 'joined' | 'subquery'`

This controls **HOW related data is fetched**

---

## 🔹 `lazy='select'` (default)

👉 Loads data **only when accessed**

```python
posts = relationship("Post", lazy="select")
```

### Query behavior:

```python
users = session.query(User).all()   # 1 query

for u in users:
    print(u.posts)  # 🔥 NEW query for each user
```

### SQL:

```
SELECT * FROM users;
SELECT * FROM posts WHERE user_id=1;
SELECT * FROM posts WHERE user_id=2;
...
```

⚠️ Problem: **N+1 query issue**

---

## 🔹 `lazy='joined'`

👉 Uses **JOIN to fetch everything in one query**

```python
posts = relationship("Post", lazy="joined")
```

### SQL:

```
SELECT users.*, posts.*
FROM users
LEFT OUTER JOIN posts ON users.id = posts.user_id;
```

### Pros:

✅ Single query
❌ Duplicate data (user repeated for each post)

---

## 🔹 `lazy='subquery'`

👉 Loads related data in **separate query using subquery**

```python
posts = relationship("Post", lazy="subquery")
```

### SQL:

```
SELECT * FROM users;

SELECT posts.*
FROM posts
JOIN (SELECT id FROM users) AS anon
ON posts.user_id = anon.id;
```

### Pros:

✅ Avoids N+1
❌ Slightly heavier than selectin

---

# ⚡ IMPORTANT:

👉 In modern SQLAlchemy, prefer:

* `selectinload()` instead of `subquery`

---

# 🚀 3. `joinedload()`

👉 Query-time version of `lazy='joined'`

```python
from sqlalchemy.orm import joinedload

users = session.query(User).options(
    joinedload(User.posts)
).all()
```

### Behavior:

* Forces JOIN **only for this query**
* Does NOT change model permanently

### Use when:

✅ You ALWAYS need related data
❌ Bad for large collections (too much duplication)

---

# 🚀 4. `selectinload()` ⭐ (MOST IMPORTANT)

👉 Best general-purpose eager loading

```python
from sqlalchemy.orm import selectinload

users = session.query(User).options(
    selectinload(User.posts)
).all()
```

### SQL:

```
SELECT * FROM users;

SELECT * FROM posts WHERE user_id IN (1,2,3,...);
```

### Pros:

✅ Avoids N+1
✅ Efficient
✅ No duplication
✅ Best for large datasets

👉 This is the **recommended approach in production**

---

# 🚀 5. `contains_eager()` (ADVANCED)

👉 Used when YOU manually write JOIN and tell SQLAlchemy:

> “I already joined this — use it as relationship data”

---

### Example:

```python
from sqlalchemy.orm import contains_eager

query = (
    session.query(User)
    .join(User.posts)
    .options(contains_eager(User.posts))
)

users = query.all()
```

### Why needed?

Without `contains_eager()`:

* SQLAlchemy ignores joined data
* Still triggers extra queries

With it:

* Uses your JOIN result directly

---

# 🧠 When to Use What (VERY IMPORTANT)

| Situation            | Best Option        |
| -------------------- | ------------------ |
| Default behavior     | `lazy='select'`    |
| Small related data   | `joinedload()`     |
| Large collections    | `selectinload()` ⭐ |
| Complex custom joins | `contains_eager()` |
| Avoid (mostly)       | `subquery`         |

---

# 🔥 Real Example (Interview-Level)

### Problem:

Get users + posts efficiently

---

### ❌ Bad (N+1)

```python
users = session.query(User).all()
for u in users:
    print(u.posts)
```

---

### ✅ Best

```python
users = session.query(User).options(
    selectinload(User.posts)
).all()
```

---

# 🧠 Key Takeaways

* `relationship()` → defines link
* `lazy` → default loading strategy
* `joinedload()` → JOIN (1 query)
* `selectinload()` → IN query (BEST ⭐)
* `contains_eager()` → manual JOIN control

---

If you want, I can next:
✅ Show **N+1 problem with real numbers (performance test)**
✅ Or give **FastAPI production patterns using these**
✅ Or design a **complex schema (school system) using all loading types**
