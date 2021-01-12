from enum import Enum
from typing import Optional, List
from functools import lru_cache

from pydantic import Field

from social_network.settings import settings

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import UserQueries

from .crud import CRUDManager
from .hobbies import Hobby


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class User(BaseModel):
    _table_name = 'users'
    _fields = ('id', 'first_name', 'last_name', 'age', 'city', 'gender')

    first_name: str
    last_name: Optional[str]
    city: Optional[str]
    gender: Optional[Gender]
    age: int = Field(..., ge=1, le=200)
    hobbies: List[Hobby] = Field(default_factory=list)


class UserManager(CRUDManager):
    model = User
    queries = {}

    # TODO: settings as param
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
