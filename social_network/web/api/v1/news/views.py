from typing import Optional, List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_utils.cbv import cbv

from social_network.db.models import (
    New,
    User,
    AddedPostNewPayload,
)
from social_network.db.managers import NewsManager, UserManager
from social_network.services.kafka import KafkaProducer

from ..depends import (
    get_user,
    get_kafka_producer,
    get_news_manager,
    get_user_manager
)
from .models import NewCreatePayload, NewsQueryParams
from ..utils import authorize_only

router = APIRouter()


# TODO: indempotet requests in all places
@cbv(router)
class NewsViewSet:
    kafka_producer: KafkaProducer = Depends(get_kafka_producer)
    user_: Optional[User] = Depends(get_user)
    news_manager: NewsManager = Depends(get_news_manager)
    user_manager: UserManager = Depends(get_user_manager)

    @router.post('/', response_model=New, status_code=201,
                 responses={
                     201: {'description': 'Hobby created.'},
                     401: {'description': 'Unauthorized.'},
                 })
    @authorize_only
    async def create(self, p: NewCreatePayload) -> New:
        payload = AddedPostNewPayload(author=self.user_.get_short(),
                                      text=p.text)
        new = New.from_payload(payload)
        await self.news_manager.create_from_model(new)
        new.populated, new.stored = True, True
        await self.kafka_producer.send(new.json())
        return new

    @router.get('/', response_model=List[New], responses={
        200: {'description': 'List of news.'},
    })
    @authorize_only
    async def list(self, q: NewsQueryParams = Depends(NewsQueryParams)) \
            -> List[New]:
        return await self.news_manager.list(author_ids=[self.user_.id],
                                            order=q.order,
                                            limit=q.paginate_by,
                                            offset=q.offset)

    @router.get('/feed/', response_model=List[New], responses={
        200: {'description': 'List of news.'},
    })
    @authorize_only
    async def feed(self, q: NewsQueryParams = Depends(NewsQueryParams)) \
            -> List[New]:
        friends_ids = await self.user_manager.get_friends_ids(self.user_.id)
        return await self.news_manager.list(author_ids=friends_ids,
                                            order=q.order,
                                            limit=q.paginate_by,
                                            offset=q.offset)
