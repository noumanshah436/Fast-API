Great! Here's a clean, modular FastAPI application structure for full **CRUD operations** using **psycopg v3**, **Pydantic models**, and best practices (separation of concerns, reusable base class, async database access).

---

### 📁 Project Structure

```
fastapi_psycopg_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py         # Async DB connection context manager
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py         # Base DB model class with CRUD
│   │   └── user_model.py         # User Pydantic + table logic
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py        # Pydantic request/response models
│   └── routes/
│       ├── __init__.py
│       └── user_routes.py        # User API endpoints
│
└── requirements.txt
```

---

### 1. `db/connection.py`

```python
# app/db/connection.py

from contextlib import asynccontextmanager
from psycopg import AsyncConnection
from psycopg.rows import dict_row
import os

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/mydb")

@asynccontextmanager
async def get_postgres_conn():
    async with await AsyncConnection.connect(POSTGRES_URL, row_factory=dict_row) as conn:
        yield conn
```

---

### 2. `models/base_model.py`

```python
# app/models/base_model.py

from typing import Any, Optional, ClassVar
from psycopg import AsyncConnection

class BaseModel:
    db_table: ClassVar[str]

    @classmethod
    async def get_by_id(cls, conn: AsyncConnection, id: int) -> Optional[dict]:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM {cls.db_table} WHERE id = %s", (id,))
            return await cur.fetchone()

    @classmethod
    async def insert(cls, conn: AsyncConnection, data: dict) -> dict:
        keys = data.keys()
        values = tuple(data.values())
        placeholders = ', '.join(['%s'] * len(keys))
        columns = ', '.join(keys)

        query = f"INSERT INTO {cls.db_table} ({columns}) VALUES ({placeholders}) RETURNING *"
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            return await cur.fetchone()

    @classmethod
    async def update(cls, conn: AsyncConnection, id: int, data: dict) -> Optional[dict]:
        set_clause = ', '.join([f"{key} = %s" for key in data])
        values = tuple(data.values()) + (id,)

        query = f"UPDATE {cls.db_table} SET {set_clause} WHERE id = %s RETURNING *"
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            return await cur.fetchone()

    @classmethod
    async def delete(cls, conn: AsyncConnection, id: int) -> bool:
        query = f"DELETE FROM {cls.db_table} WHERE id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (id,))
            return cur.rowcount > 0
```

---

### 3. `models/user_model.py`

```python
# app/models/user_model.py

from app.models.base_model import BaseModel

class UserModel(BaseModel):
    db_table = "users"
```

---

### 4. `schemas/user_schema.py`

```python
# app/schemas/user_schema.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

---

### 5. `routes/user_routes.py`

```python
# app/routes/user_routes.py

from fastapi import APIRouter, HTTPException
from app.db.connection import get_postgres_conn
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(payload: UserCreate):
    async with get_postgres_conn() as conn:
        user = await UserModel.insert(conn, payload.dict())
        return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    async with get_postgres_conn() as conn:
        user = await UserModel.get_by_id(conn, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate):
    async with get_postgres_conn() as conn:
        user = await UserModel.update(conn, user_id, payload.dict(exclude_unset=True))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    async with get_postgres_conn() as conn:
        success = await UserModel.delete(conn, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted"}
```

---

### 6. `main.py`

```python
# app/main.py

from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(title="FastAPI + Psycopg v3")

app.include_router(user_router)
```

---

### 7. `requirements.txt`

```txt
fastapi
uvicorn
psycopg[binary]
pydantic
```

---

### ✅ To Run the App

1. Ensure the `users` table exists:

   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name TEXT NOT NULL,
       email TEXT NOT NULL
   );
   ```

2. Start the server:

   ```bash
   uvicorn app.main:app --reload
   ```

---

Let me know if you want:

* connection pooling (`psycopg.Pool`)
* dependency injection via `Depends`
* auto migrations with Alembic or SQLModel
* Dockerization

Would you like a zip of this structure?
