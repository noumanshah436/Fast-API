Perfect — here's how to create a new PostgreSQL database named `fastapi_pg` and update your FastAPI app to use it.

---

## ✅ Step 1: Create `fastapi_pg` Database

### 1.1 Login to PostgreSQL using the `nouman` user:

```bash
psql -h localhost -U nouman -d postgres -W
```

Enter password: `noumanrehman042`

---

### 1.2 Run this SQL command to create the new database:

```sql
CREATE DATABASE fastapi_pg;
```

You should see:

```
CREATE DATABASE
```

Then exit the psql shell:

```sql
\q
```

---

## ✅ Step 2: Update FastAPI App to Use `fastapi_pg`

### 2.1 Open `app/db/connection.py` and update the connection string:

```python
# app/db/connection.py

from contextlib import asynccontextmanager
from psycopg import AsyncConnection
from psycopg.rows import dict_row
import os

POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nouman:noumanrehman042@localhost:5432/fastapi_pg"
)

@asynccontextmanager
async def get_postgres_conn():
    async with await AsyncConnection.connect(POSTGRES_URL, row_factory=dict_row) as conn:
        yield conn
```

---

## ✅ Step 3: Create the `users` Table in `fastapi_pg`

```bash
psql -h localhost -U nouman -d fastapi_pg -W
```

Then run:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
```

Then exit:

```sql
\q
```

---

## ✅ Step 4: Run Your FastAPI App

```bash
uvicorn app.main:app --reload
```

Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
And test the endpoints using your new `fastapi_pg` database!

---

Let me know if you want to:

* Create a `.env` file for cleaner config
* Add Docker support
* Scaffold automatic database initialization via Python or Alembic
