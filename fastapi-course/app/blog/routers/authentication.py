from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from blog import schemas, database, models, token
from blog.hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print("login method called")
    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    # generate the jwt token and return it
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# **********************

# OAuth2PasswordRequestForm:

# OAuth2PasswordRequestForm is a FastAPI class that's designed to handle requests for OAuth2 password grants.

# It automatically validates and parses incoming requests that include a username and password in the request body.

# **********************

# login parameters explaination:

# The request parameter is automatically filled with data from the incoming request body using FastAPI's built-in OAuth2PasswordRequestForm.

# The db parameter is filled by invoking the get_db function, which is a dependency that provides an SQLAlchemy database session

# **********************
