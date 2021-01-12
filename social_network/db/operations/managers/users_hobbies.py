from functools import lru_cache
from typing import List

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import HobbyQueries

from social_network.settings import settings

from .crud import CRUDManager, CRUD


class UserHobby(BaseModel):
    _table_name = 'users_hobbies_mtm'
    _fields = ('id', 'user_id', 'hobby_id')

    user_id: int
    hobby_id: int



class UsersHobbyManager(CRUDManager):
    model = UserHobby
    # TODO: refactor crud
    queries = {}

    async def create(self, name: str) -> UserHobby:
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
