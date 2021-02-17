from uuid import uuid4
from datetime import datetime
from typing import Optional, List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_utils.cbv import cbv

from social_network.db.models import (
    New,
    User,
    NewsType,
    AddedPostNewPayload,
    TIMESTAMP_FORMAT
)
from social_network.db.managers import NewsManager

from ..depends import (
    get_user,
    get_news_manager
)
from .models import NewCreatePayload, NewsQueryParams
from ..utils import authorize_only

router = APIRouter()


@cbv(router)
class NewsViewSet:
    user: Optional[User] = Depends(get_user)
    news_manager: NewsManager = Depends(get_news_manager)

    @router.post('/', response_model=New, status_code=201,
                 responses={
                     201: {'description': 'Hobby created.'},
                     401: {'description': 'Unauthorized.'},
                 })
    @authorize_only
    async def create(self, p: NewCreatePayload) -> New:
        payload = AddedPostNewPayload(author=self.user.get_short(), text=p.text)
        now = datetime.now().strftime(TIMESTAMP_FORMAT)
        new = await self.news_manager.create(
            self.user.id,
            news_type=NewsType.ADDED_POST,
            payload=payload,
            created=now
        )
        # TODO: send to followers
        return new

    @router.get('/', response_model=List[New], responses={
        200: {'description': 'List of news.'},
    })
    @authorize_only
    async def list(self, q: NewsQueryParams = Depends(NewsQueryParams)) \
            -> List[New]:
        return await self.news_manager.list(author_id=self.user.id,
                                            order=q.order,
                                            limit=q.paginate_by,
                                            offset=q.offset)
