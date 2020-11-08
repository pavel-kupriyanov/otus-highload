from typing import Tuple, Any, Optional

from .db import (
    BaseDatabaseConnector,
    DatabaseError,
    DatabaseResponse
)


class BaseManager:

    def __init__(self, db: BaseDatabaseConnector):
        self.db = db

    async def _execute(self,
                       query: str,
                       params: Optional[Tuple[Any, ...]] = None,
                       last_row_id=False
                       ) -> DatabaseResponse:
        try:
            return await self.db.make_query(query, params,
                                            last_row_id=last_row_id)
        except Exception as e:
            raise DatabaseError from e
