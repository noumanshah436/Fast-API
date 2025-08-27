Let's extend the app by adding a `Post` model, where each post belongs to a `User` (one-to-many relationship).

We’ll:

* Create a `posts` table
* Add Pydantic schemas for posts
* Extend the base model logic if needed
* Create endpoints to:

  * Create a post for a user
  * Get all posts for a user
  * Get, update, and delete individual posts

---

### 🗃️ Database Schema

Make sure this table exists in your PostgreSQL DB:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
```

---

### 🔁 File Structure Changes

```
app/
├── models/
│   └── post_model.py
├── schemas/
│   └── post_schema.py
└── routes/
    └── post_routes.py
```

---

### 1. `models/post_model.py`

```python
# app/models/post_model.py

from app.models.base_model import BaseModel

class PostModel(BaseModel):
    db_table = "posts"
```

---

### 2. `schemas/post_schema.py`

```python
# app/schemas/post_schema.py

from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
```

---

### 3. `routes/post_routes.py`

```python
# app/routes/post_routes.py

from fastapi import APIRouter, HTTPException
from app.db.connection import get_postgres_conn
from app.models.post_model import PostModel
from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/user/{user_id}", response_model=PostResponse)
async def create_post_for_user(user_id: int, payload: PostCreate):
    async with get_postgres_conn() as conn:
        data = payload.dict()
        data["user_id"] = user_id
        post = await PostModel.insert(conn, data)
        return post

@router.get("/user/{user_id}", response_model=list[PostResponse])
async def get_user_posts(user_id: int):
    async with get_postgres_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
            return await cur.fetchall()

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    async with get_postgres_conn() as conn:
        post = await PostModel.get_by_id(conn, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, payload: PostUpdate):
    async with get_postgres_conn() as conn:
        post = await PostModel.update(conn, post_id, payload.dict(exclude_unset=True))
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    async with get_postgres_conn() as conn:
        success = await PostModel.delete(conn, post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post deleted"}
```

---

### 4. Update `main.py`

```python
# app/main.py

from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.post_routes import router as post_router

app = FastAPI(title="FastAPI + Psycopg v3")

app.include_router(user_router)
app.include_router(post_router)
```

---

### 🧪 Sample Requests

#### ✅ Create Post for User

```http
POST /posts/user/1
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the body of my post."
}
```

#### ✅ Get All Posts for User

```http
GET /posts/user/1
```

#### ✅ Update Post

```http
PUT /posts/2
Content-Type: application/json

{
  "title": "Updated Title"
}
```

---

Would you like to:

* Add pagination to `/posts/user/{user_id}`?
* Nest posts under `/users/{id}/posts` instead?
* Include user info in the post response?

Let me know if you'd like me to generate a downloadable project zip for this.
