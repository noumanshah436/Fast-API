from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.post_routes import router as post_router

app = FastAPI(title="FastAPI + Psycopg v3")

app.include_router(user_router)
app.include_router(post_router)