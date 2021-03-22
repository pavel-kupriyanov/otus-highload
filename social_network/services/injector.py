from typing import Type, TypeVar, List

from social_network.db.connectors_storage import ConnectorsStorage
from social_network.settings import Settings

from .base import BaseService, BaseController
from .kafka import KafkaProducer, KafkaConsumersService
from .redis import RedisService
from .rabbitmq import RabbitMQPProducer
from .ws import FeedWebSocketService

M = TypeVar('M')


class DependencyInjector(BaseController):
    connectors_storage: ConnectorsStorage
    kafka_producer: KafkaProducer
    rabbit_producer: RabbitMQPProducer
    redis_service: RedisService
    ws_service: FeedWebSocketService
    kafka_consumer_service: KafkaConsumersService

    def __init__(self, conf: Settings):
        self.conf = conf
        self.connectors_storage = ConnectorsStorage()
        self.redis_service = RedisService(conf.REDIS)
        self.rabbit_producer = RabbitMQPProducer(conf.RABBIT)
        self.kafka_producer = KafkaProducer(conf.KAFKA)
        self.kafka_consumer_service = KafkaConsumersService(
            self.conf.KAFKA,
            self.conf.NEWS_CACHE,
            connectors_storage=self.connectors_storage,
            redis_service=self.redis_service,
            kafka_producer=self.kafka_producer,
            rabbit_producer=self.rabbit_producer
        )
        self.ws_service = FeedWebSocketService()

    @property
    def services(self) -> List[BaseService]:
        return [
            self.kafka_producer,
            self.kafka_consumer_service,
            self.redis_service,
            self.ws_service,
            self.rabbit_producer
        ]

    async def start(self):
        connectors_storage = self.connectors_storage
        await connectors_storage.create_connector(self.conf.DATABASE.MASTER)

        for conf in self.conf.DATABASE.SLAVES:
            await connectors_storage.create_connector(conf)

        await super().start()

    def get_manager(self, cls: Type[M]) -> M:
        return cls(self.connectors_storage, self.conf)
