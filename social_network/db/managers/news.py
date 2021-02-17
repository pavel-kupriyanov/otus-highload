from uuid import uuid4
from typing import Dict, Type, Optional

from ..crud import CRUDManager
from ..models import (
    New,
    NewsType,
    Payload,
    AddedPostNewPayload,
    AddedHobbyNewPayload,
    AddedFriendNewPayload
)

GET_USER_NEWS = '''
    SELECT id, author_id, type, payload, created FROM news
    WHERE author_id = %s
'''

GET_NEWS = '''
    SELECT id, author_id, type, payload, created FROM news
'''


class NewsManager(CRUDManager):
    model = New
    auto_id = False

    payload_mapping: Dict[NewsType, Type[Payload]] = {
        NewsType.ADDED_POST: AddedPostNewPayload,
        NewsType.ADDED_HOBBY: AddedHobbyNewPayload,
        NewsType.ADDED_FRIEND: AddedFriendNewPayload
    }

    async def create(self, id: str, author_id: int, news_type: NewsType,
                     payload: Payload, created: str) -> New:
        params = (id, author_id, news_type, payload.json(), created)
        query = self._make_create_query()
        await self.execute(query, params, raise_if_empty=False)
        return await self._get(id, read_only=False)

    # TODO: fix limit in other places
    async def list(self, author_id: Optional[int] = None, order_by='created',
                   order='DESC', limit=None, offset=0):
        params, query = tuple(), GET_NEWS
        if author_id:
            params, query = (author_id,), GET_USER_NEWS
        limit = limit or self.conf.BASE_PAGE_LIMIT
        return await self._list(params, query, order_by=order_by, order=order,
                                limit=limit, offset=offset)
