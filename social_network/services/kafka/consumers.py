from random import sample
from asyncio import AbstractEventLoop, create_task, gather
from typing import Dict, Tuple, List
from json import loads

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from aioredis import Redis

from social_network.settings import KafkaSettings
from social_network.db.models import New, NewsType
from social_network.db.managers import NewsManager, HobbiesManager, UserManager
from social_network.db.connectors_storage import ConnectorsStorage
from social_network.services.redis import RedisService, RedisKeys

from .consts import Topic
from .producer import KafkaProducer
from ..base import BaseService


class BaseKafkaConsumer(BaseService):
    group_id: str
    consumer: AIOKafkaConsumer
    topics: Tuple[str]

    def __init__(self,
                 conf: KafkaSettings,
                 loop: AbstractEventLoop,
                 **kwargs):
        self.conf = conf
        self.loop = loop
        self.task = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=f'{self.conf.HOST}:{self.conf.PORT}',
            loop=self.loop,
            group_id=self.group_id,
            consumer_timeout_ms=5000
        )
        await self.consumer.start()
        self.task = create_task(self.process())

    async def close(self):
        self.task.cancel()
        await self.consumer.stop()

    @staticmethod
    def parse(record: ConsumerRecord) -> Dict:
        return loads(record.value)

    async def process(self):
        async for record in self.consumer:
            try:
                await self._process(self.parse(record))
            except Exception as e:
                print(repr(e))
                raise
            await self.consumer.commit()

    async def _process(self, msg: Dict):
        raise NotImplemented


class BaseNewsKafkaConsumer(BaseKafkaConsumer):
    topics = (Topic.News,)


class PopulateNewsKafkaConsumer(BaseKafkaConsumer):
    group_id = 'populate'
    topics = (Topic.Populate,)

    def __init__(self,
                 conf: KafkaSettings,
                 loop: AbstractEventLoop,
                 connectors_storage: ConnectorsStorage,
                 kafka_producer: KafkaProducer):
        super().__init__(conf, loop)
        self.kafka_producer = kafka_producer
        self.hobbies_manager = HobbiesManager(connectors_storage)
        self.user_manager = UserManager(connectors_storage)

    async def _process(self, raw_new: Dict):
        print(f'To populated: {raw_new["id"]}')
        new = New(**raw_new)
        if not new.populated:
            await self.populate(new)
        print(f'After populate: {new}')
        await self.kafka_producer.send(new.json())

    async def populate(self, new: New):
        if new.type == NewsType.ADDED_HOBBY:
            await self.populate_add_hobby(new)
        else:
            await self.populate_add_friend(new)
        new.populated = True

    async def populate_add_friend(self, new: New):
        for user_type in ('author', 'new_friend'):
            user_id = getattr(new.payload, user_type)
            if isinstance(user_id, int):
                user = await self.user_manager.get(user_id)
                setattr(new.payload, user_type, user.get_short())

    async def populate_add_hobby(self, new: New):
        hobby_id = new.payload.hobby
        if isinstance(hobby_id, int):
            new.payload.hobby = await self.hobbies_manager.get(hobby_id)


class NewsKafkaDatabaseConsumer(BaseNewsKafkaConsumer):
    group_id = 'news_database'

    def __init__(self,
                 conf: KafkaSettings,
                 loop: AbstractEventLoop,
                 connectors_storage: ConnectorsStorage):
        super().__init__(conf, loop)
        self.news_manager = NewsManager(connectors_storage)

    async def _process(self, raw_new: Dict):
        new = New(**raw_new)
        if new.stored:
            return
        print(f'Write into db: {new}')
        await self.news_manager.create_from_model(new)


class NewsKafkaCacheConsumer(BaseNewsKafkaConsumer):
    group_id = 'news_cache'
    MAX_FOLLOWERS = 100
    MAX_FEED_SIZE = 100

    def __init__(self,
                 conf: KafkaSettings,
                 loop: AbstractEventLoop,
                 connector_storage: ConnectorsStorage,
                 redis_service: RedisService):
        super().__init__(conf, loop)
        self.redis: Redis = redis_service
        self.users_manager = UserManager(connector_storage)

    async def _process(self, raw_new: Dict):
        new = New(**raw_new)
        follower_ids = await self.get_follower_ids(new.author_id)

        add_tasks = []
        for follower_id in follower_ids:
            task = create_task(self.add_new_to_feed(follower_id, new))
            add_tasks.append(task)

        await gather(*add_tasks)

        print(f'Written into cache: {new.id}')

    async def add_new_to_feed(self, follower_id: int, new: New):
        feed = await self.redis.hget(RedisKeys.USER_FEED, follower_id) or []
        feed = sorted(feed, key=lambda raw_new: raw_new['created'])
        offset = len(feed) - self.MAX_FEED_SIZE - 1
        if offset > 0:
            feed = feed[offset:]

        feed.append(new.dict())

        await self.redis.hset(RedisKeys.USER_FEED, follower_id, feed)

    async def get_follower_ids(self, user_id: int) -> List[int]:
        followers = await self.redis.hget(RedisKeys.FOLLOWERS, user_id)
        if not followers:
            followers = await self.users_manager.get_friends_ids(user_id)
            await self.redis.hset(RedisKeys.FOLLOWERS, user_id, followers)
        else:
            print('from cache')
        print(followers)
        if len(followers) > self.MAX_FOLLOWERS:
            followers = sample(followers, self.MAX_FOLLOWERS)

        return followers
