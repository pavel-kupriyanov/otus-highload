from enum import Enum
from collections import namedtuple
from typing import List
from functools import lru_cache

from ..base import BaseModel
from ..db import BaseDatabaseConnector
from ..queries import FriendRequestQueries

from .crud import BaseCRUDManager, CRUD


class FriendRequestStatus(str, Enum):
    WAITING = 'WAITING'
    DECLINED = 'DECLINED'


class FriendRequestModel(BaseModel):
    _parsing_tuple = namedtuple('_', 'id, from_user, to_user, status')

    from_user: int
    to_user: int
    status: FriendRequestStatus


class FriendRequestManager(BaseCRUDManager):
    fields = ('id', 'from_user', 'to_user', 'status')
    model = FriendRequestModel
    queries = {
        CRUD.RETRIEVE: FriendRequestQueries.GET_FRIEND_REQUEST,
        CRUD.LIST: FriendRequestQueries.GET_FRIEND_REQUESTS,
        CRUD.DELETE: FriendRequestQueries.DROP_FRIEND_REQUEST,
        CRUD.CREATE: FriendRequestQueries.CREATE_FRIEND_REQUEST,
        CRUD.UPDATE: FriendRequestQueries.UPDATE_FRIEND_REQUEST
    }

    async def create(self, from_user: int, to_user: int,
                     base_status=FriendRequestStatus.WAITING) \
            -> FriendRequestModel:
        return await self._create((from_user, to_user, base_status))

    async def update(self, id: int, status: FriendRequestStatus) \
            -> FriendRequestModel:
        return await self._update(id, (status, id))

    async def list_for_user_exclude_status(self, user_id: int,
                                           status: FriendRequestStatus) \
            -> List[FriendRequestModel]:
        query = FriendRequestQueries.GET_NON_STATUS_FRIEND_REQUESTS
        return await self._list((user_id, user_id, status), query)

    async def list_for_user(self, user_id: int) -> List[FriendRequestModel]:
        return await self._list((user_id, user_id))

    async def delete(self, id: int):
        await self._delete(id)

    async def get(self, id: int) -> FriendRequestModel:
        return await self._get(id)


@lru_cache(1)
def get_friend_request_manager(
        connector: BaseDatabaseConnector) -> FriendRequestManager:
    return FriendRequestManager(connector)
