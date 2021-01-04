from collections import namedtuple
from typing import Optional, List
from functools import lru_cache

from social_network.settings import settings

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import UserQueries

from .crud import BaseCRUDManager, CRUD


# TODO: additional user info
class UserModel(BaseModel):
    _parsing_tuple = namedtuple('_', 'id, first_name, last_name')

    first_name: str
    last_name: Optional[str]


class UserManager(BaseCRUDManager):
    fields = ('id', 'first_name', 'last_name')
    model = UserModel
    queries = {
        CRUD.LIST: UserQueries.GET_USERS
    }

    # TODO: update, retrieve
    async def list(self,
                   search='',
                   order_by='last_name',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[UserModel]:
        return await self._list((search, search),
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)


@lru_cache(1)
def get_user_manager(connector: BaseDatabaseConnector) -> UserManager:
    return UserManager(connector)
