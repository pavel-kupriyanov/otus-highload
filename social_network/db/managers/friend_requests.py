from typing import List

from ..crud import CRUDManager, CRUD

from ..queries import FriendRequestQueries
from ..models import FriendRequest, FriendRequestStatus


class FriendRequestManager(CRUDManager):
    model = FriendRequest
    queries = {
        CRUD.LIST: FriendRequestQueries.GET_FRIEND_REQUESTS,
        CRUD.UPDATE: FriendRequestQueries.UPDATE_FRIEND_REQUEST
    }

    async def create(self, from_user: int, to_user: int,
                     base_status=FriendRequestStatus.WAITING) \
            -> FriendRequest:
        return await self._create((from_user, to_user, base_status))

    async def update(self, id: int, status: FriendRequestStatus) \
            -> FriendRequest:
        return await self._update(id, (status, id))

    async def list_for_user_exclude_status(self, user_id: int,
                                           status: FriendRequestStatus) \
            -> List[FriendRequest]:
        query = FriendRequestQueries.GET_NON_STATUS_FRIEND_REQUESTS
        return await self._list((user_id, user_id, status), query)

    async def list_for_user(self, user_id: int) -> List[FriendRequest]:
        return await self._list((user_id, user_id))
