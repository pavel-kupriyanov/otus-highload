from enum import Enum
from typing import Dict, Tuple, Any, List, Optional

from social_network.settings import settings

from ..base import BaseManager, BaseModel, M
from ..db import RowsNotFoundError
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
        query = self.queries.get(CRUD.CREATE) or create_query(self.model)
        id = await self.execute(query, params, last_row_id=True)
        return await self._get(id)

    async def _update(self, id: int, params: Tuple[Any, ...]) -> M:
        await self.execute(self.queries[CRUD.UPDATE], params,
                           raise_if_empty=False)
        return await self._get(id)

    async def _get(self, id: int) -> M:
        model: BaseModel = self.model
        query = self.queries.get(CRUD.RETRIEVE) or get_query(self.model)
        rows = await self.execute(query, (id,))
        return model.from_db(rows[0])

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
        rows = await self.execute(query, params, raise_if_empty=False)
        return [self.model.from_db(row) for row in rows]

    async def _delete(self, id: int):
        query = self.queries.get(CRUD.DELETE) or delete_query(self.model)
        await self.execute(query, (id,), raise_if_empty=False)


def get_fields_without_id(model: BaseModel) -> Tuple[str, ...]:
    return tuple((f for f in model._fields if f != 'id'))


def get_query(model: BaseModel) -> str:
    return f'''
        SELECT {", ".join(model._fields)} FROM {model._table_name}
        WHERE id = %s;
        '''


def create_query(model: BaseModel) -> str:
    fields = get_fields_without_id(model)
    return f'''
        INSERT INTO {model._table_name}({", ".join(fields)})
        VALUES ({", ".join('%s' for _ in fields)});
        SELECT LAST_INSERT_ID();
        '''


def delete_query(model: BaseModel) -> str:
    return f'''
        DELETE FROM {model._table_name}
        WHERE id = %s
        '''
