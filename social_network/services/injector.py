from asyncio import get_running_loop
from typing import Type, TypeVar, List

from social_network.db.connectors_storage import ConnectorsStorage
from social_network.settings import Settings

from .base import BaseService
from .kafka import KafkaProducer, KafkaConsumersService
from .redis import RedisService
from .ws import FeedWebSocketService

M = TypeVar('M')


class DependencyInjector(BaseService):
    connectors_storage: ConnectorsStorage
    kafka_producer: KafkaProducer
    redis_service: RedisService
    ws_service: FeedWebSocketService
    kafka_consumer_service: KafkaConsumersService

    def __init__(self, conf: Settings):
        self.conf = conf
        self.connectors_storage = ConnectorsStorage()
        self.redis_service = RedisService(conf.REDIS)
        self.kafka_producer = KafkaProducer(conf.KAFKA)
        self.kafka_consumer_service = KafkaConsumersService(
            self.conf.KAFKA,
            self.conf.NEWS_CACHE,
            loop=get_running_loop(),
            connectors_storage=self.connectors_storage,
            redis_service=self.redis_service,
            kafka_producer=self.kafka_producer
        )
        self.ws_service = FeedWebSocketService()

    @property
    def services(self) -> List[BaseService]:
        return [
            self.kafka_producer,
            self.kafka_consumer_service,
            self.redis_service,
            self.ws_service
        ]

    async def start(self):
        connectors_storage = self.connectors_storage
        await connectors_storage.create_connector(self.conf.DATABASE.MASTER)

        for conf in self.conf.DATABASE.SLAVES:
            await connectors_storage.create_connector(conf)
        for service in self.services:
            await service.start()

    async def close(self):
        for service in self.services:
            await service.close()

    def get_manager(self, cls: Type[M]) -> M:
        return cls(self.connectors_storage, self.conf)
