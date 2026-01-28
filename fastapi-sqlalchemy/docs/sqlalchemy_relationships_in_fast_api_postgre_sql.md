This guide teaches SQLAlchemy relationships step by step in a FastAPI + PostgreSQL setup. We start from zero and build up relationships gradually, explaining *why* each relationship exists, *when* to use it, and *how* SQLAlchemy behaves internally.

---

## 0. Assumptions & Stack

- FastAPI
- SQLAlchemy 2.x (async)
- PostgreSQL
- `asyncpg` driver

We will focus on **data modeling and relationships**, not FastAPI routing yet.

---

## 1. Base Setup (Foundation)

Every SQLAlchemy model must inherit from a **Base**.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

This Base:
- Tracks all models
- Is used by Alembic to generate migrations
- Enables ORM features like relationships

---

## 2. Simple Model (No Relationships)

Let’s start with a single table.

### User model

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
```

### What’s happening
- `id` → Primary key (auto-incremented)
- No relationships yet
- Each row is independent

This is **flat data**.

---

## 3. One-to-Many Relationship

### Scenario

> One **User** can have many **Posts**
> A **Post** belongs to one **User**

This is the **most common relationship**.

---

### Step 1: Create the child table

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="posts")
```

### Step 2: Update the parent

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)

    posts = relationship("Post", back_populates="user")
```

---

### How this works internally

| Concept | Meaning |
|------|-------|
| `ForeignKey` | Enforces DB-level link |
| `relationship()` | ORM-level navigation |
| `back_populates` | Two-way sync |

Now you can:

```python
user.posts      # list[Post]
post.user       # User
```

---

## 4. One-to-One Relationship

### Scenario

> One **User** has one **Profile**

Technically this is a **one-to-many with a uniqueness constraint**.

---

### Profile model

```python
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile")
```

### User update

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)
```

---

### Key flags explained

| Flag | Why |
|----|----|
| `unique=True` | Enforces one-to-one in DB |
| `uselist=False` | ORM returns single object |

---

## 5. Many-to-Many Relationship

### Scenario

> Users can belong to many **Teams**
> Teams can have many **Users**

This requires a **junction table**.

---

### Association table

```python
from sqlalchemy import Table

user_team = Table(
    "user_team",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)
```

---

### Team model

```python
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    users = relationship("User", secondary=user_team, back_populates="teams")
```

### User update

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

    teams = relationship("Team", secondary=user_team, back_populates="users")
```

---

### What SQLAlchemy does

- No model for `user_team`
- Auto-joins when accessing `.teams` or `.users`
- Handles inserts/deletes automatically

---

## 6. Association Object (Many-to-Many with Extra Fields)

### Scenario

> User belongs to Team **with a role**

Now the junction table becomes a **real model**.

---

### Membership model

```python
class Membership(Base):
    __tablename__ = "memberships"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    team_id = Column(ForeignKey("teams.id"), primary_key=True)
    role = Column(String)

    user = relationship("User", back_populates="memberships")
    team = relationship("Team", back_populates="memberships")
```

### User & Team updates

```python
class User(Base):
    memberships = relationship("Membership", back_populates="user")

class Team(Base):
    memberships = relationship("Membership", back_populates="team")
```

---

## 7. Cascade Behavior (VERY IMPORTANT)

```python
posts = relationship(
    "Post",
    back_populates="user",
    cascade="all, delete-orphan",
)
```

### What this means

| Action | Result |
|----|----|
| Delete user | Delete posts |
| Remove post from list | Delete post |

Without cascade → orphan rows ❌

---

## 8. Lazy Loading vs Eager Loading

```python
relationship("Post", lazy="select")
relationship("Post", lazy="joined")
relationship("Post", lazy="selectin")
```

### Recommended

| Case | Strategy |
|----|----|
| Lists | `selectin` |
| Single | `joined` |
| Default | `select` |

---

## 9. Common Mistakes

❌ Missing `back_populates`
❌ Forgetting `ForeignKey`
❌ Using cascade blindly
❌ Loading too much data eagerly

---

## 10. Mental Model (IMPORTANT)

- **ForeignKey** = Database rule
- **relationship()** = Python navigation
- SQLAlchemy NEVER guesses joins
- You must define both sides

---

## What’s Next

If you want, next we can:
- Add **async queries** in FastAPI
- Visualize schema diagrams
- Handle **soft deletes**
- Design **audit / activity tables**
- Apply this to your Sankey / activity schema

Just tell me the next step 👌

