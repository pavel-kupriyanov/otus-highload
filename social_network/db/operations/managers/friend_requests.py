from enum import Enum
from collections import namedtuple
from typing import Optional, List
from functools import lru_cache

from ..base import BaseManager, BaseModel
from ..db import BaseDatabaseConnector
from ..queries import FriendRequestQueries


class FriendRequestStatus(str, Enum):
    WAITING = 'WAITING'
    DECLINED = 'DECLINED'


class FriendRequestModel(BaseModel):
    _parsing_tuple = namedtuple('_', 'id, from_user, to_user, status')

    from_user: int
    to_user: int
    status: FriendRequestStatus


class FriendRequestManager(BaseManager):

    async def create(self, from_user: int, to_user: int,
                     base_status=FriendRequestStatus.WAITING) \
            -> FriendRequestModel:
        params = (from_user, to_user, base_status)
        id = self.execute(FriendRequestQueries.CREATE_FRIEND_REQUEST, params,
                          last_row_id=True)
        return FriendRequestModel(
            id=id,
            from_user=from_user,
            to_user=to_user,
            status=base_status
        )

    async def update(self, id: int, status: FriendRequestStatus):
        await self.execute(FriendRequestQueries.UPDATE_FRIEND_REQUEST,
                           (status, id))

    async def delete(self, id: int):
        await self.execute(FriendRequestQueries.DROP_FRIEND_REQUEST, (id,))

    async def list(self, user_id: int,
                   exclude_status: Optional[FriendRequestStatus] = None
                   ) -> List[FriendRequestModel]:
        query = FriendRequestQueries.GET_FRIEND_REQUESTS
        params = [user_id, user_id]
        if exclude_status:
            query = FriendRequestQueries.GET_NON_STATUS_FRIEND_REQUESTS
            params.append(exclude_status)

        requests = await self.execute(query, params)
        return [FriendRequestModel.from_db(request) for request in requests]

    async def get(self, id: int) -> FriendRequestModel:
        request = await self.execute(FriendRequestQueries.GET_FRIEND_REQUEST,
                                     (id,))
        return FriendRequestModel.from_db(request)


@lru_cache(1)
def get_friend_request_manager(
        connector: BaseDatabaseConnector) -> FriendRequestManager:
    return FriendRequestManager(connector)
