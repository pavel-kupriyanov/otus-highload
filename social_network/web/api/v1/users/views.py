from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_utils.cbv import cbv

from social_network.db import (
    UserManager,
    FriendshipManager,
    User,
)

from .models import UsersPayload
from ..depends import (
    get_user_manager_depends,
    get_friendship_manager_depends
)

router = APIRouter()


@cbv(router)
class UserViewSet:
    user_manager: UserManager = Depends(get_user_manager_depends)
    friendship_manager: FriendshipManager = Depends(
        get_friendship_manager_depends)

    @router.get('/', response_model=List[User], responses={
        200: {'description': 'List of users.'},
    })
    async def users(self, p: UsersPayload = UsersPayload()):
        offset = (p.page - 1) * p.paginate_by
        return await self.user_manager.search_list(search=p.search,
                                                   order=p.order,
                                                   order_by=p.order_by,
                                                   limit=p.paginate_by,
                                                   offset=offset)

    @router.get('/{user_id}', response_model=User, responses={
        200: {'description': 'User.'},
        404: {'description': 'User not found.'}
    })
    async def user(self, user_id: int) -> User:
        return await self.user_manager.get(user_id)
