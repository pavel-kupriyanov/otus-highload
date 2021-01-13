from typing import Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi_utils.cbv import cbv

from social_network.db.models import (
    Friendship,
    FriendRequestStatus,
    FriendRequest
)
from social_network.db.managers import (
    FriendRequestManager,
    FriendshipManager
)
from social_network.db.excpetions import (
    DatabaseError,
    RowsNotFoundError
)

from ..depends import (
    get_friend_request_manager,
    get_user_id
)
from .models import FriendRequestPostPayload

from ..depends import get_friendship_manager
from ..utils import authorize_only

router = APIRouter()


@cbv(router)
class FriendRequestViewSet:
    user_id: Optional[int] = Depends(get_user_id)
    friend_request_manager: FriendRequestManager = Depends(
        get_friend_request_manager
    )
    friendship_manager: FriendshipManager = Depends(
        get_friendship_manager
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
        try:
            await self.friendship_manager \
                .get_by_participants(self.user_id, p.user_id)
        except RowsNotFoundError:
            pass
        else:
            raise HTTPException(400, detail='Users already friends.')

        try:
            return await self.friend_request_manager \
                .create(self.user_id, p.user_id)
        except DatabaseError:
            raise HTTPException(404, detail='User not found or request '
                                            'already exists.')

    @router.delete('/{id}', status_code=204, responses={
        204: {'description': 'Friend request cancelled.'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only request owner can cancel it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def cancel(self, id: int):
        request = await self.friend_request_manager.get(id)
        if not is_request_creator(request, self.user_id):
            raise HTTPException(403, detail='You are not allowed to delete'
                                            ' request')
        await self.friend_request_manager.delete(id)

    @router.get('/{id}', status_code=200, responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only participants can get it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def get(self, id: int) -> FriendRequest:
        request = await self.friend_request_manager.get(id)
        if not is_request_participant(request, self.user_id):
            raise HTTPException(403, detail='Not allowed')
        return request

    @router.put('/decline/{id}', status_code=204, responses={
        204: {'description': 'Success'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only request target can decline it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def decline(self, id: int):
        request = await self.friend_request_manager.get(id)
        if not is_request_target(request, self.user_id):
            raise HTTPException(403, 'Not allowed')
        await self.friend_request_manager.update(id,
                                                 FriendRequestStatus.DECLINED)

    @router.put('/accept/{id}', response_model=Friendship,
                status_code=201,
                responses={
                    201: {'description': 'Success'},
                    401: {'description': 'Unauthorized.'},
                    403: {'description': 'Only request target can accept it'},
                    404: {'description': 'Request not found.'}
                })
    @authorize_only
    async def accept(self, id: int) -> Friendship:
        request = await self.friend_request_manager.get(id)

        if not is_request_target(request, self.user_id):
            raise HTTPException(403, detail='Not allowed')

        await self.friend_request_manager.delete(id)
        return await self.friendship_manager.create(request.to_user,
                                                    request.from_user)


def is_request_creator(request: FriendRequest, user_id: int) -> bool:
    return request.from_user == user_id


def is_request_target(request: FriendRequest, user_id: int) -> bool:
    return request.to_user == user_id


def is_request_participant(request: FriendRequest, user_id: int) -> bool:
    return user_id in (request.from_user, request.to_user)
