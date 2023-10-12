from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# as we are running our project from app folder as root
# we will use ./blog.db
SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

#  A base class for declarative models. It will be used as a base class for all the models in the project.
Base = declarative_base()

# A function to get a database session for use in FastAPI dependency injection.
# It yields a database session and ensures it is closed after use.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# https://fastapi.tiangolo.com/tutorial/sql-databases/
