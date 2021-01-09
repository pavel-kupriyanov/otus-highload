from enum import Enum
from typing import List
from functools import lru_cache

from ..base import BaseModel
from ..db import BaseDatabaseConnector, RowsNotFoundError
from ..queries import FriendRequestQueries

from .crud import BaseCRUDManager, CRUD


class FriendRequestStatus(str, Enum):
    WAITING = 'WAITING'
    DECLINED = 'DECLINED'


class FriendRequest(BaseModel):
    _table_name = 'friend_requests'
    _fields = ('id', 'from_user', 'to_user', 'status')

    from_user: int
    to_user: int
    status: FriendRequestStatus


class FriendRequestManager(BaseCRUDManager):
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

    async def delete(self, id: int):
        await self._delete(id)

    async def get(self, id: int) -> FriendRequest:
        return await self._get(id)

    async def get_by_user_ids(self, from_user: int, to_user: int) \
            -> FriendRequest:
        query = FriendRequestQueries.GET_FRIEND_REQUEST_BY_USERS
        requests = await self.execute(query, (from_user, to_user))
        if not requests:
            raise RowsNotFoundError(f'{type(self.model)} not found.')
        return FriendRequest.from_db(requests[0])


@lru_cache(1)
def get_friend_request_manager(
        connector: BaseDatabaseConnector) -> FriendRequestManager:
    return FriendRequestManager(connector)
