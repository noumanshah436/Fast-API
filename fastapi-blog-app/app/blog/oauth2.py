from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from blog import token
from blog import database
from fastapi import Depends
from sqlalchemy.orm import Session

# OAuth2PasswordBearer is used to create an instance of an authentication dependency, which can be used in your route functions to require authentication.
# The tokenUrl parameter in OAuth2PasswordBearer is used to specify the endpoint where clients can request a token.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# This function will be used as a dependency in other route functions to require authentication.
# oauth2_scheme is used as a dependency to get the token from the request.

def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # data will contain the jwt token string
    print("oauth#get_current_user called with data:" + data)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception, db)


# In the FastAPI route definition, the oauth2_scheme (OAuth2PasswordBearer) is used as a dependency to extract the token from the request.
# The token is expected to be included in the Authorization header using the Bearer scheme.

# ***************************************************************************************************

# Here's a quick breakdown: (first read flow of token varification file)

# 1) oauth2_scheme Instance:

# Created using OAuth2PasswordBearer(tokenUrl="login").
# This instance is essentially a reusable dependency that knows how to extract and validate OAuth2 bearer tokens.

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# *********************************

# 2) get_current_user Function:

# Defined to use oauth2_scheme as a dependency to get the token from the request.
# It prints the token and then calls token.verify_token for validation.
# If validation fails, it raises an HTTPException indicating a 401 Unauthorized status.

# *********************************

# 3) Using get_current_user as a Dependency:

# In your route functions, you use Depends(get_current_user) to make sure the user is authenticated before proceeding with the route logic.

# @router.get('/', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return blog.get_all(db)

# *********************************

# This pattern is a good separation of concerns. The get_current_user function is responsible for extracting and validating the token, while your route functions are concerned with the application's business logic. It makes your code modular, readable, and easy to maintain. Each part of your application has a well-defined responsibility.

# ***************************************************************************************************

