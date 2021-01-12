from typing import Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi_utils.cbv import cbv

from social_network.db.models import Friendship
from social_network.db.managers import FriendshipManager
from social_network.db.excpetions import RowsNotFoundError

from ..depends import get_user_id

from ..depends import get_friendship_manager
from ..utils import authorize_only

router = APIRouter()


@cbv(router)
class FriendshipViewSet:
    user_id: Optional[int] = Depends(get_user_id)
    friendship_manager: FriendshipManager = Depends(
        get_friendship_manager
    )

    @router.delete('/{id}', status_code=204, responses={
        204: {'description': 'Friendship cancelled.'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only friendship participant can cancel it'},
        404: {'description': 'Request not found.'}
    })
    @authorize_only
    async def delete(self, id: int):
        request = await self.friendship_manager.get(id)
        if self.user_id not in (request.user_id, request.friend_id):
            raise HTTPException(403, detail='Not allowed')
        try:
            reverse_request = await self.friendship_manager \
                .get_by_participants(request.friend_id, request.user_id)
            await self.friendship_manager.delete(reverse_request.id)
        except RowsNotFoundError:
            pass
        await self.friendship_manager.delete(id)

    @router.get('/{id}', status_code=200, responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized.'},
        403: {'description': 'Only participants can get it'},
        404: {'description': 'Friendship not found.'}
    })
    @authorize_only
    async def get(self, id: int) -> Friendship:
        request = await self.friendship_manager.get(id)
        if self.user_id not in (request.user_id, request.friend_id):
            raise HTTPException(403, 'Not allowed')
        return request
