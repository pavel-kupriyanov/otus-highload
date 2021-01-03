from typing import Tuple, Any, Optional

from aiomysql import DatabaseError as RawDatabaseError

from .db import (
    BaseDatabaseConnector,
    DatabaseError,
    DatabaseResponse
)


class BaseManager:

    def __init__(self, db: BaseDatabaseConnector):
        self.db = db

    async def execute(self,
                      query: str,
                      params: Optional[Tuple[Any, ...]] = None,
                      last_row_id=False
                      ) -> DatabaseResponse:
        try:
            return await self.db.make_query(query, params,
                                            last_row_id=last_row_id)
        except RawDatabaseError as e:
            raise DatabaseError(e.args) from e
