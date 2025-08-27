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