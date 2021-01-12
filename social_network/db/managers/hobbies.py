from typing import List

from social_network.settings import settings

from ..crud import CRUDManager, CRUD

from ..models import Hobby
from ..queries import HobbyQueries


class HobbiesManager(CRUDManager):
    model = Hobby
    # TODO: refactor crud
    queries = {
        CRUD.LIST: HobbyQueries.GET_HOBBIES
    }

    async def create(self, name: str) -> Hobby:
        return await self._create((name.capitalize(),))

    async def list(self,
                   name='',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[Hobby]:
        return await self._list((name,), order=order, limit=limit,
                                offset=offset)
