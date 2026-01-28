from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.uvicorn_filters import HealthCheckFilter
from src.routers import (
    healthcheck_api,
)

# Hide healthcheck logs from uvicorn access logs
logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # await db.connect_to_database()

    yield  # App runs here

    # Shutdown
    # await db.close_database_connection()


# Initialize the FastAPI app
app = FastAPI(title="Fastapi", version="1.0.0", lifespan=lifespan)

# allow cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# creating all models
app.include_router(router=healthcheck_api.router)
