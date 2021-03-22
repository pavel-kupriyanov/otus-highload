from asyncio import AbstractEventLoop
from typing import List, Type

from social_network.settings import KafkaSettings, NewsCacheSettings
from social_network.db.connectors_storage import ConnectorsStorage

from .producer import KafkaProducer
from .consumers import (
    BaseKafkaConsumer,
    NewsKafkaDatabaseConsumer,
    NewsKafkaCacheConsumer,
    PopulateNewsKafkaConsumer
)
from ..redis import RedisService
from ..base import BaseService


class KafkaConsumersService(BaseService):
    conf: KafkaSettings
    loop: AbstractEventLoop
    connectors_storage: ConnectorsStorage
    redis_service: RedisService
    kafka_producer: KafkaProducer
    consumer_classes: List[Type[BaseKafkaConsumer]]
    consumers: List[BaseKafkaConsumer]

    def __init__(self,
                 conf: KafkaSettings,
                 news_conf: NewsCacheSettings,
                 loop: AbstractEventLoop,
                 kafka_producer: KafkaProducer,
                 connectors_storage: ConnectorsStorage,
                 redis_service: RedisService):
        self.conf = conf
        self.news_conf = news_conf
        self.loop = loop
        self.kafka_producer = kafka_producer
        self.connectors_storage = connectors_storage
        self.redis_service = redis_service
        self.consumers = []

    def init_consumers(self) -> List[BaseKafkaConsumer]:
        conf, loop = self.conf, self.loop
        connectors_storage = self.connectors_storage
        kafka_producer = self.kafka_producer
        db_consumer = NewsKafkaDatabaseConsumer(conf, loop, connectors_storage)
        cache_consumer = NewsKafkaCacheConsumer(conf, self.news_conf, loop,
                                                connectors_storage,
                                                self.redis_service)
        populate_consumer = PopulateNewsKafkaConsumer(
            conf, loop, connectors_storage, kafka_producer
        )
        return [db_consumer, cache_consumer, populate_consumer]

    async def start(self):
        self.consumers = self.init_consumers()
        for consumer in self.consumers:
            await consumer.start()

    async def close(self):
        for consumer in self.consumers:
            await consumer.close()
