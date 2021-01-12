from functools import lru_cache
from typing import List

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import HobbyQueries

from social_network.settings import settings

from .crud import CRUDManager, CRUD


class Hobby(BaseModel):
    _table_name = 'hobbies'
    _fields = ('id', 'name')

    name: str


class HobbyManager(CRUDManager):
    model = Hobby
    # TODO: refactor crud
    queries = {
        CRUD.LIST: HobbyQueries.GET_HOBBIES
    }

    async def create(self, name: str) -> Hobby:
        return await self._create((name.capitalize(),))

    async def list(self,
                   name='',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[Hobby]:
        return await self._list((name,), order=order, limit=limit,
                                offset=offset)


# TODO: class method?
@lru_cache(1)
def get_hobby_manager(connector: BaseDatabaseConnector) -> HobbyManager:
    return HobbyManager(connector)
