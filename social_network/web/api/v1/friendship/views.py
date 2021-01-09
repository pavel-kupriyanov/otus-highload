from typing import Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi_utils.cbv import cbv

from social_network.db import (
    FriendRequestManager,
    FriendRequest,
    DatabaseError,
    FriendshipManager,
    Friendship
)
from social_network.db.operations.managers.friend_requests import \
    FriendRequestStatus

from ..depends import (
    get_friend_request_manager_depends,
    get_user_id
)
from .models import FriendRequestPostPayload

from ..depends import get_friendship_manager_depends
from ..utils import authorize_only

router = APIRouter()


# TODO: refactor it

@cbv(router)
class FriendshipViewSet:
    user_id: Optional[int] = Depends(get_user_id)
    friend_request_manager: FriendRequestManager = Depends(
        get_friend_request_manager_depends
    )
    friendship_manager: FriendshipManager = Depends(
        get_friendship_manager_depends
    )

    async def already_friends(self, user_id1: int, user_id2: int) -> bool:
        return await self.friendship_manager.already_friends(
            user_id1, user_id2
        )

    @router.post('/', response_model=FriendRequest, status_code=201,
                 responses={
                     201: {'description': 'Friend request created.'},
                     400: {'description': 'Already friends.'},
                     401: {'description': 'Unauthorized.'},
                     404: {'description': 'User not found.'}
                 })
    @authorize_only
    async def create(self, p: FriendRequestPostPayload) -> FriendRequest:
        if await self.already_friends(self.user_id, p.user_id):
            raise HTTPException(400, detail='Users already friends.')

        try:
            return await self.friend_request_manager.create(self.user_id,
                                                            p.user_id)
        except DatabaseError:
            raise HTTPException(404, detail='User not found or request'
                                            ' already created.')

    @router.delete('/{request_id}', status_code=204, responses={
        204: {'description': 'Friend request cancelled.'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only request owner can cancel it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def cancel(self, request_id: int):
        try:
            request = await self.friend_request_manager.get(request_id)
        except DatabaseError:
            raise HTTPException(404, detail='request not found')
        if not is_request_creator(request, self.user_id):
            raise HTTPException(403, detail='You are not allowed to delete'
                                            ' request')
        await self.friend_request_manager.delete(request_id)

    @router.get('/{request_id}', status_code=200, responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only participants can get it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def get(self, request_id: int) -> FriendRequest:
        try:
            request = await self.friend_request_manager.get(request_id)
        except DatabaseError:
            raise HTTPException(404, 'Request not found')
        if not is_request_participant(request, self.user_id):
            raise HTTPException(403, 'Not allowed')
        return request

    @router.put('/decline/{request_id}', status_code=204, responses={
        204: {'description': 'Success'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only request target can decline it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def decline(self, request_id: int):
        try:
            request = await self.friend_request_manager.get(request_id)
        except DatabaseError:
            raise HTTPException(404, 'Request not found')
        if not is_request_target(request, self.user_id):
            raise HTTPException(403, 'Not allowed')
        await self.friend_request_manager.update(request_id,
                                                 FriendRequestStatus.DECLINED)

    @router.put('/accept/{request_id}', response_model=Friendship,
                status_code=201,
                responses={
                    201: {'description': 'Success'},
                    401: {'description': 'Unauthorized.'},
                    403: {'description': 'Only request target can accept it'},
                    404: {'description': 'Request not found.'}
                })
    @authorize_only
    async def accept(self, request_id: int):
        try:
            request = await self.friend_request_manager.get(request_id)
        except DatabaseError:
            raise HTTPException(404, 'Request not found')

        if not is_request_target(request, self.user_id):
            raise HTTPException(403, 'Not allowed')

        # TODO: transaction
        await self.friend_request_manager.delete(request_id)
        return await self.friendship_manager.create(request.from_user,
                                                    request.to_user)


def is_request_creator(request: FriendRequest, user_id: int) -> bool:
    return request.from_user == user_id


def is_request_target(request: FriendRequest, user_id: int) -> bool:
    return request.to_user == user_id


def is_request_participant(request: FriendRequest, user_id: int) -> bool:
    return user_id in (request.from_user, request.to_user)
