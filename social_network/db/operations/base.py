from typing import Optional, Tuple, Any
from functools import lru_cache

import aiomysql

from social_network.settings import (
    settings,
    DatabaseSettings
)


class Database:

    # TODO: gracefully shutdown

    def __init__(self, conf: DatabaseSettings):
        self.conf = conf

    async def make_query(self, query: str, max_rows: Optional[int] = None)\
            -> Tuple[Tuple[Any, ...]]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:  # type: aiomysql.Connection
            async with conn.cursor() as cursor:  # type: aiomysql.Cursor
                rowcount = await cursor.execute(query)
                return await cursor.fetchmany(max_rows or rowcount)

    @lru_cache(1)
    async def get_pool(self) -> aiomysql.Pool:
        c = self.conf
        return await aiomysql.create_pool(host=c.HOST, port=c.PORT, user=c.USER,
                                          password=c.PASSWORD, db=c.NAME,
                                          maxsize=c.MAX_CONNECTIONS)

    async def close(self):
        pool = await self.get_pool()
        pool.close()
        await pool.wait_closed()


# TODO: factory instead hardcode
database = Database(settings.DATABASE)
