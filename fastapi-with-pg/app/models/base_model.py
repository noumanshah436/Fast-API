from typing import Optional, ClassVar
from psycopg import AsyncConnection

class BaseModel:
    db_table: ClassVar[str]

    @classmethod
    async def get_by_id(cls, conn: AsyncConnection, id: int) -> Optional[dict]:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM {cls.db_table} WHERE id = %s", (id,))
            return await cur.fetchone()

    @classmethod
    async def insert(cls, conn: AsyncConnection, data: dict) -> dict:
        keys = data.keys()
        values = tuple(data.values())
        placeholders = ', '.join(['%s'] * len(keys))
        columns = ', '.join(keys)
        query = f"INSERT INTO {cls.db_table} ({columns}) VALUES ({placeholders}) RETURNING *"
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            return await cur.fetchone()

    @classmethod
    async def update(cls, conn: AsyncConnection, id: int, data: dict) -> Optional[dict]:
        set_clause = ', '.join([f"{key} = %s" for key in data])
        values = tuple(data.values()) + (id,)
        query = f"UPDATE {cls.db_table} SET {set_clause} WHERE id = %s RETURNING *"
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            return await cur.fetchone()

    @classmethod
    async def delete(cls, conn: AsyncConnection, id: int) -> bool:
        query = f"DELETE FROM {cls.db_table} WHERE id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (id,))
            return cur.rowcount > 0