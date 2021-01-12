from ..crud import CRUDManager
from ..queries import FriendshipQueries
from ..models import Friendship


class FriendshipManager(CRUDManager):
    model = Friendship
    queries = {}

    async def create(self, user_id: int, friend_id: int) -> Friendship:
        await self._create((friend_id, user_id))
        return await self._create((user_id, friend_id))

    async def get_by_participants(self, user_id: int, friend_id: int) \
            -> Friendship:
        query = FriendshipQueries.GET_FRIENDSHIP
        friendships = await self.execute(query, (user_id, friend_id))
        return Friendship.from_db(friendships[0])
