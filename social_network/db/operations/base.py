from typing import Optional, Tuple, Any
from functools import lru_cache

import aiomysql

from social_network.settings.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


class Database:

    # TODO: gracefully shutdown

    async def make_query(self, query: str, max_rows: Optional[int] = None) -> Tuple[Tuple[Any, ...]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:  # type: aiomysql.Connection
            async with conn.cursor() as cursor:  # type: aiomysql.Cursor
                rowcount = await cursor.execute(query)
                return await cursor.fetchmany(max_rows or rowcount)

    @staticmethod
    @lru_cache(1)
    async def get_pool() -> aiomysql.Pool:
        # TODO: min size, max size
        return await aiomysql.create_pool(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                          password=DB_PASSWORD, db=DB_NAME)

    async def close(self):
        pool = await self.get_pool()
        pool.close()
        await pool.wait_closed()


# TODO: factory instead hardcode
database = Database()
