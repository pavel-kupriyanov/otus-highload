from functools import lru_cache

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import FriendshipQueries

from .crud import BaseCRUDManager


class Friendship(BaseModel):
    _table_name = 'friendships'
    _fields = ('id', 'user_id', 'friend_id')

    user_id: int
    friend_id: int


class FriendshipManager(BaseCRUDManager):
    model = Friendship
    queries = {}

    async def create(self, user_id: int, friend_id: int) -> Friendship:
        await self._create((friend_id, user_id))
        return await self._create((user_id, friend_id))

    async def delete(self, id: int):
        await self._delete(id)

    # TODO: add public methods for crud manager for base actions
    async def get(self, id: int) -> Friendship:
        return await self._get(id)

    async def get_by_participants(self, user_id: int, friend_id: int) \
            -> Friendship:
        query = FriendshipQueries.GET_FRIENDSHIP
        friendships = await self.execute(query, (user_id, friend_id))
        return Friendship.from_db(friendships[0])


@lru_cache(1)
def get_friendship_manager(
        connector: BaseDatabaseConnector) -> FriendshipManager:
    return FriendshipManager(connector)
