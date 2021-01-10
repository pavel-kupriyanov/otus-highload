from typing import Optional, List
from functools import lru_cache

from social_network.settings import settings

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import UserQueries

from .crud import BaseCRUDManager


# TODO: additional user info
class User(BaseModel):
    _table_name = 'users'
    _fields = ('id', 'first_name', 'last_name')

    first_name: str
    last_name: Optional[str]


class UserManager(BaseCRUDManager):
    model = User
    queries = {}

    # TODO: update
    async def list(self,
                   first_name='',
                   last_name='',
                   friend_id: int = None,
                   order_by='last_name',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[User]:
        params = [first_name, last_name]
        query = UserQueries.GET_USERS
        if friend_id:
            params.append(friend_id)
            query = UserQueries.GET_FRIENDS
        return await self._list(tuple(params),
                                query=query,
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)

    async def list_by_ids(self,
                          ids: List[int],
                          order_by='last_name',
                          order='ASC',
                          limit=settings.BASE_PAGE_LIMIT,
                          offset=0) -> List[User]:
        query = UserQueries.GET_USERS_BY_IDS
        return await self._list((ids,), query,
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)

    async def get(self, id: int) -> User:
        return await self._get(id)


@lru_cache(1)
def get_user_manager(connector: BaseDatabaseConnector) -> UserManager:
    return UserManager(connector)
