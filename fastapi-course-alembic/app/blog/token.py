from datetime import datetime, timedelta
from jose import JWTError, jwt
from blog import schemas, database, models
from sqlalchemy.orm import Session


# python-jose to generate and verify the JWT tokens in Python

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "10767d7839aa5da89bf58cc6ed0430f22d58b5640bc22e78af7e884f95bc398d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

get_db = database.get_db


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("payload:", payload)
        # {'sub': 'noumanrehman042@gmail.com', 'exp': 1697135184}

        email: str = payload.get("sub")

        if not email:
            raise credentials_exception

        token_data = schemas.TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(
        models.User.email == token_data.email).first()

    if not user:
        raise credentials_exception

    return user


# ***************************

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#about-jwt

# ***************************

# jwt.encode:

# The jwt.encode function is used to create a new JWT
#   by encoding a Python dictionary (payload) using a specified secret key and algorithm.

# jwt.encode(claims, key, algorithm)

# i) claims: This is a dictionary containing the claims (data) that you want to include in the JWT. Common claims include "sub" (subject), "exp" (expiration time), "iss" (issuer), etc.

# ii) key: This is the secret key used for encoding the JWT. It should be kept secure because it is used to both create and verify the token.

# iii) algorithm: This specifies the cryptographic algorithm used to sign the token. Common algorithms include "HS256" (HMAC with SHA-256) and "RS256" (RSA with SHA-256).


# jwt.encode Returns:
#     str: The string representation of the header, claims, and signature.


# ***************************

# jwt.decode:

# The jwt.decode function is used to verify and decode an existing JWT,
#   extracting the claims contained within.


# jwt.decode(token, key, algorithms)

# i) token: This is the JWT that you want to decode and verify.

# ii) key: This is the secret key used for verifying the JWT's signature.

# iii) algorithms: This is a list of acceptable algorithms for verifying the token. It should match the algorithm used during encoding.


# jwt.decode Returns:
#     dict: The dict representation of the claims set, assuming the signature is valid
#         and all requested data validation passes.

# ***************************

# timedelta is generally used for calculating differences in dates

# timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
# This part creates a timedelta object, which represents a duration of time

# ***************************
