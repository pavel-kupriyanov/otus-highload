from typing import List
from functools import lru_cache

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import FriendshipQueries

from .crud import BaseCRUDManager


class Friendship(BaseModel):
    _table_name = 'friendships'
    _fields = ('id', 'user_id1', 'user_id2')

    user_id1: int
    user_id2: int


class FriendshipManager(BaseCRUDManager):
    # TODO: think about better friendship database model
    model = Friendship
    queries = {}

    async def create(self, user_id1: int, user_id2: int) -> Friendship:
        return await self._create((user_id1, user_id2))

    async def delete(self, id: int):
        await self._delete(id)

    async def list(self, user_id: int) -> List[Friendship]:
        query = FriendshipQueries.GET_FRIENDSHIPS
        return await self._list((user_id, user_id), query)

    async def already_friends(self, user_id1: int, user_id2: int) -> bool:
        params = (user_id1, user_id2, user_id2, user_id1)
        query = FriendshipQueries.GET_FRIENDSHIP_BY_IDS
        friendships = await self.execute(query, params, raise_if_empty=False)
        return bool(friendships)


@lru_cache(1)
def get_friendship_manager(
        connector: BaseDatabaseConnector) -> FriendshipManager:
    return FriendshipManager(connector)
