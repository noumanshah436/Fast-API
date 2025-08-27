# app/db/connection.py

from contextlib import asynccontextmanager
from psycopg import AsyncConnection
from psycopg.rows import dict_row
import os

POSTGRES_URL = os.getenv(
    "DATABASE_URL", "postgresql://nouman:noumanrehman042@localhost:5432/fastapi_pg"
)


@asynccontextmanager
async def get_postgres_conn():
    async with await AsyncConnection.connect(
        POSTGRES_URL, row_factory=dict_row
    ) as conn:
        yield conn
