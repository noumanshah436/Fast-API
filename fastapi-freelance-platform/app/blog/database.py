from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = 'postgresql://nouman:noumanrehman042@localhost:5432/fastapi_freelance_platform'
# TODO: use env variables
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
