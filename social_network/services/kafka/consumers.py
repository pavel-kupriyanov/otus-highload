from asyncio import AbstractEventLoop, create_task
from typing import List, Dict, Type, Tuple, Any
from datetime import datetime as dt
from json import loads

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from social_network.settings import KafkaSettings
from social_network.db.models import New, TIMESTAMP_FORMAT, NewsType
from social_network.db.managers import NewsManager, HobbiesManager, UserManager
from social_network.db.connectors_storage import ConnectorsStorage

from .consts import Topic
from .producer import KafkaProducer
from ..base import BaseService


# TODO: think about better dependency injection
class BaseKafkaConsumer(BaseService):
    group_id: str
    consumer: AIOKafkaConsumer
    topics: Tuple[str]
    depends: Dict[str, Type[Any]] = {}

    def __init__(self, conf: KafkaSettings, loop: AbstractEventLoop, **kwargs):
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
            await self._process(self.parse(record))
            await self.consumer.commit()

    async def _process(self, msg: Dict):
        raise NotImplemented


class BaseNewsKafkaConsumer(BaseKafkaConsumer):
    topics = (Topic.News,)


class PopulateNewsKafkaConsumer(BaseKafkaConsumer):
    group_id = 'populate'
    topics = (Topic.Populate,)
    depends = {
        'connectors_storage': ConnectorsStorage,
        'kafka_producer': KafkaProducer
    }

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
    depends = {
        'connectors_storage': ConnectorsStorage,
    }

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
        await self.news_manager.create(
            id=new.id,
            author_id=new.author_id,
            news_type=new.type,
            payload=new.payload,
            created=dt.fromtimestamp(new.created).strftime(TIMESTAMP_FORMAT),
        )


class NewsKafkaCacheConsumer(BaseNewsKafkaConsumer):
    group_id = 'news_cache'

    async def _process(self, raw_new: Dict):
        print(f'Written into cache: {raw_new["id"]}')


# TODO: split files

class KafkaConsumersManager(BaseService):
    conf: KafkaSettings
    consumer_classes: List[Type[BaseKafkaConsumer]]
    loop: AbstractEventLoop
    connectors_storage: ConnectorsStorage
    kafka_producer: KafkaProducer
    consumers: List[BaseKafkaConsumer]

    dependency_mapping: Dict[Any, str] = {
        ConnectorsStorage: 'connectors_storage',
        KafkaProducer: 'kafka_producer'
    }

    def __init__(self,
                 conf: KafkaSettings,
                 consumer_classes: List[Type[BaseKafkaConsumer]],
                 connectors_storage: ConnectorsStorage,
                 kafka_producer: KafkaProducer,
                 loop: AbstractEventLoop):
        self.conf = conf
        self.consumer_classes = consumer_classes
        self.connectors_storage = connectors_storage
        self.kafka_producer = kafka_producer
        self.consumers = []
        self.loop = loop

    async def start(self):
        for consumer_cls in self.consumer_classes:
            dependencies = self.resolve_dependencies(consumer_cls)
            consumer = consumer_cls(self.conf, loop=self.loop, **dependencies)
            await consumer.start()
            self.consumers.append(consumer)

    def resolve_dependencies(
            self, consumer_cls: Type[BaseKafkaConsumer]
    ) -> Dict[str, Any]:
        dependencies = {}
        for dependency in consumer_cls.depends.values():
            attr_name = self.dependency_mapping[dependency]
            dependencies[attr_name] = getattr(self, attr_name)

        return dependencies

    async def close(self):
        for consumer in self.consumers:
            await consumer.close()
