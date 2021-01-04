from enum import Enum
from typing import Dict, Tuple, Any, List, Optional

from social_network.settings import settings

from ..base import BaseManager, M
from ..db import DatabaseError
from .mixins import LimitMixin, OrderMixin


class CRUD(str, Enum):
    CREATE = 'CREATE'
    RETRIEVE = 'RETRIEVE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    LIST = 'LIST'


class BaseCRUDManager(BaseManager, LimitMixin, OrderMixin):
    model: M
    queries: Dict[CRUD, str]

    async def _create(self, params: Tuple[Any, ...]) -> M:
        id = await self.execute(self.queries[CRUD.CREATE], params,
                                last_row_id=True)
        return await self._get(id)

    async def _update(self, id: int, params: Tuple[Any, ...]) -> M:
        await self.execute(self.queries[CRUD.UPDATE], params)
        return await self._get(id)

    async def _get(self, id: int) -> M:
        rows = await self.execute(self.queries[CRUD.RETRIEVE], (id,))
        if not rows:
            raise DatabaseError(f'{type(self.model)} {id} not found.')
        return self.model.from_db(rows[0])

    async def _list(self,
                    params: Tuple[Any, ...],
                    query: Optional[str] = None,
                    order_by: str = None,
                    order: str = None,
                    limit: int = settings.BASE_PAGE_LIMIT,
                    offset: int = 0) -> List[M]:
        if query is None:
            query = self.queries[CRUD.LIST]
        if order_by and order:
            query = self.add_order(query, order_by, order)
        query = self.add_limit(query, limit, offset)
        rows = await self.execute(query, params)
        return [self.model.from_db(row) for row in rows]

    async def _delete(self, id: int):
        await self.execute(self.queries[CRUD.DELETE], (id,))
