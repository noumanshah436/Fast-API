from pydantic import BaseModel
from typing import List
from enum import Enum

class NoteInput(BaseModel):
    title: str = ''
    note_body: str = ''

class UserType(str, Enum):
    volunteer = "volunteer"
    recipient = "recipient"

class UserBase(BaseModel):
    name: str
    email: str
    city: str
    country: str
    age: int
    user_type: UserType
    phone: str
    address: str
    motivation: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

