from typing import Optional, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi_utils.cbv import cbv

from social_network.db import (
    FriendRequest,
    DatabaseError,
    Hobby,
    HobbyManager
)

from ..depends import (
    get_user_id,
    get_hobby_manager_depends
)
from .models import HobbyCreatePayload, HobbyQueryParams

from ..utils import authorize_only

router = APIRouter()


@cbv(router)
class HobbiesViewSet:
    user_id: Optional[int] = Depends(get_user_id)
    hobby_manager: HobbyManager = Depends(get_hobby_manager_depends)

    @router.post('/', response_model=Hobby, status_code=201,
                 responses={
                     201: {'description': 'Hobby created.'},
                     400: {'description': 'Already created.'},
                     401: {'description': 'Unauthorized.'},
                 })
    @authorize_only
    async def create(self, p: HobbyCreatePayload) -> Hobby:
        try:
            return await self.hobby_manager.create(p.name)
        except DatabaseError:
            raise HTTPException(400, detail='Hobby already exists.')

    @router.get('/{id}', responses={
        200: {'description': 'Success'},
        404: {'description': 'Hobby not found.'}
    })
    async def get(self, id: int) -> FriendRequest:
        return await self.hobby_manager.get(id)

    @router.get('/', response_model=List[Hobby], responses={
        200: {'description': 'List of hobbies.'},
    })
    async def list(self, q: HobbyQueryParams = Depends(HobbyQueryParams)):
        # TODO: offset as payload method
        offset = (q.page - 1) * q.paginate_by
        return await self.hobby_manager.list(name=q.name,
                                             order=q.order,
                                             limit=q.paginate_by,
                                             offset=offset)