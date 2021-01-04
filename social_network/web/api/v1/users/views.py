from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_utils.cbv import cbv

from social_network.db import (
    UserManager,
    UserModel,
)

from .models import UsersPayload
from ..utils import (
    get_user_manager_depends,
)

router = APIRouter()


# TODO: update self
@cbv(router)
class UserViewSet:
    user_manager: UserManager = Depends(get_user_manager_depends)

    @router.get('/', response_model=List[UserModel], responses={
        200: {'description': 'List of users'},
    })
    async def users(self, p: UsersPayload = UsersPayload()):
        offset = (p.page - 1) * p.paginate_by
        return await self.user_manager.list(search=p.search,
                                            order=p.order,
                                            order_by=p.order_by,
                                            limit=p.paginate_by,
                                            offset=offset)
