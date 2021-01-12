from functools import lru_cache

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import UserHobbyQueries

from .crud import CRUDManager


class UserHobby(BaseModel):
    _table_name = 'users_hobbies_mtm'
    _fields = ('id', 'user_id', 'hobby_id')

    user_id: int
    hobby_id: int


class UsersHobbyManager(CRUDManager):
    model = UserHobby
    # TODO: refactor crud
    queries = {}

    async def create(self, user_id: int, hobby_id: int) -> UserHobby:
        return await self._create((user_id, hobby_id))

    async def delete_by_ids(self, user_id: int, hobby_id: int):
        params = (user_id, hobby_id)
        return await self.execute(UserHobbyQueries.DROP_USER_HOBBY, params,
                                  raise_if_empty=False)


# TODO: class method?
@lru_cache(1)
def get_user_hobby_manager(connector: BaseDatabaseConnector) \
        -> UsersHobbyManager:
    return UsersHobbyManager(connector)
