from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_utils.cbv import cbv

from social_network.db import UserManager, User

from .models import UsersQueryParams
from ..depends import get_user_manager_depends

router = APIRouter()


@cbv(router)
class UserViewSet:
    user_manager: UserManager = Depends(get_user_manager_depends)

    @router.get('/', response_model=List[User], responses={
        200: {'description': 'List of users.'},
    })
    async def users(self, q: UsersQueryParams = Depends(UsersQueryParams)):
        offset = (q.page - 1) * q.paginate_by
        return await self.user_manager.list(first_name=q.first_name,
                                            last_name=q.last_name,
                                            friend_id=q.friends_of,
                                            order=q.order,
                                            order_by=q.order_by,
                                            limit=q.paginate_by,
                                            offset=offset)

    @router.get('/{id}', response_model=User, responses={
        200: {'description': 'User.'},
        404: {'description': 'User not found.'}
    })
    async def user(self, id: int) -> User:
        return await self.user_manager.get(id)
