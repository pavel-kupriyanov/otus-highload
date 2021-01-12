from typing import List

from social_network.settings import settings

from ..queries import UserQueries

from ..crud import CRUDManager
from ..models import User


class UserManager(CRUDManager):
    model = User
    queries = {}

    # TODO: settings as param
    async def list(self,
                   first_name='',
                   last_name='',
                   friend_id: int = None,
                   order_by='last_name',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[User]:
        params = [first_name, last_name]
        query = UserQueries.GET_USERS
        if friend_id:
            params.append(friend_id)
            query = UserQueries.GET_FRIENDS
        return await self._list(tuple(params),
                                query=query,
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)
