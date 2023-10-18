from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError

from schemas import NoteInput, UserBase, UserResponse

from model.database import DBSession
from model import models

app = FastAPI()

origins = [
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/users")
def all_users():
    db = DBSession()

    try:
        users = db.query(models.User).all()
    finally:
        db.close()

    return users


@app.post("/users", response_model=UserResponse)
async def create_user(user_create: UserBase):
    db = DBSession()
    try:
        db_user = models.User(**user_create.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Email address already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
    return db_user
