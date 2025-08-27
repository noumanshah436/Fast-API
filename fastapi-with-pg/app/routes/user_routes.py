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