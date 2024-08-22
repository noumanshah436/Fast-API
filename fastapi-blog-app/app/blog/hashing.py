from passlib.context import CryptContext

# This FastAPI code is for handling password hashing and verification using the passlib library with the bcrypt hashing scheme.

# CryptContext class is used for securely hashing and verifying passwords.

# An instance of CryptContext is created with the bcrypt hashing scheme specified.
# The deprecated="auto" parameter indicates that the library should automatically handle any deprecated hashing methods.
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)



# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
