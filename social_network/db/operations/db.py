from typing import Optional, Tuple, Any, Union
from functools import lru_cache

import aiomysql

from social_network.settings import (
    Settings,
    DatabaseSettings
)


class DatabaseError(Exception):
    pass


class RowsNotFoundError(Exception):
    pass


Rows = Tuple[Tuple[Any, ...]]
DatabaseResponse = Union[Rows, int]


class BaseDatabaseConnector:

    async def make_query(self,
                         query_template: str,
                         params: Optional[Tuple[Any, ...]] = None,
                         max_rows: Optional[int] = None,
                         last_row_id=False,
                         raise_if_empty=True) \
            -> DatabaseResponse:
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError


class DatabaseConnector(BaseDatabaseConnector):

    # TODO: gracefully shutdown

    def __init__(self, conf: DatabaseSettings):
        self.conf = conf
        self.pool = None

    async def make_query(self,
                         query_template: str,
                         params: Optional[Tuple[Any, ...]] = None,
                         max_rows: Optional[int] = None,
                         last_row_id=False,
                         raise_if_empty=True) \
            -> DatabaseResponse:
        pool = await self.get_pool()
        async with pool.acquire() as conn:  # type: aiomysql.Connection
            async with conn.cursor() as cursor:  # type: aiomysql.Cursor
                rowcount = await cursor.execute(query_template, params)
                if last_row_id:
                    return cursor.lastrowid
                data = await cursor.fetchmany(max_rows or rowcount)

                if raise_if_empty and not data:
                    raise RowsNotFoundError
                return data

    async def get_pool(self) -> aiomysql.Pool:
        if self.pool is None:
            self.pool = await self._create_pool()
        return self.pool

    async def _create_pool(self) -> aiomysql.Pool:
        c = self.conf
        password = c.PASSWORD.get_secret_value()
        return await aiomysql.create_pool(host=c.HOST, port=c.PORT,
                                          user=c.USER, password=password,
                                          db=c.NAME, maxsize=c.MAX_CONNECTIONS,
                                          autocommit=True)

    async def close(self):
        pool = await self.get_pool()
        pool.close()
        await pool.wait_closed()


@lru_cache(1)
def get_connector(settings: Settings) -> BaseDatabaseConnector:
    return DatabaseConnector(settings.DATABASE)
