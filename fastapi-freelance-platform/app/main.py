from fastapi import FastAPI
from blog import models   # blog is our module
from blog.database import engine
from blog.routers import blog, user, authentication

app = FastAPI()

# create all tables in the database(blog.db file) as per our models
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
# app.include_router(blog.router)
app.include_router(user.router)
