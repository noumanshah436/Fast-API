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