from typing import Tuple, Any, Optional

from aiomysql import DatabaseError as RawDatabaseError

from .db import (
    BaseDatabaseConnector,
    DatabaseError,
    DatabaseResponse
)


class BaseManager:
    fields: Optional[Tuple[str]]
    order = ('ASC', 'DESC')

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

    def _add_order(self, query: str, field: str, order='ASC') -> str:
        if field not in self.fields or order not in self.order:
            raise ValueError(f'Invalid values: {field}, {order}')
        return '\n'.join((query, f'ORDER BY {field} {order}'))

    def _add_limit(self, query: str, limit: int = 100, offset: int = 0) -> str:
        for param in (limit, offset):
            if not isinstance(param, int) or param < 0:
                raise ValueError(f'Invalid values: {limit}, {offset}')
        return '\n'.join((query, f'LIMIT {limit} OFFSET {offset}'))
