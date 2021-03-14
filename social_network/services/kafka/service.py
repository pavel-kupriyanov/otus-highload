from asyncio import AbstractEventLoop
from typing import List, Type

from social_network.settings import KafkaSettings, NewsCacheSettings

from .consumers import (
    BaseKafkaConsumer,
    NewsKafkaDatabaseConsumer,
    NewsKafkaCacheConsumer,
    PopulateNewsKafkaConsumer
)
from ..base import BaseService
from ..injector import DependencyInjector


class KafkaConsumersService(BaseService):
    conf: KafkaSettings
    loop: AbstractEventLoop
    injector: DependencyInjector
    consumer_classes: List[Type[BaseKafkaConsumer]]
    consumers: List[BaseKafkaConsumer]

    def __init__(self,
                 conf: KafkaSettings,
                 news_conf: NewsCacheSettings,
                 loop: AbstractEventLoop,
                 injector: DependencyInjector):
        self.conf = conf
        self.news_conf = news_conf
        self.loop = loop
        self.injector = injector
        self.consumers = []

    def init_consumers(self) -> List[BaseKafkaConsumer]:
        conf, loop, injector = self.conf, self.loop, self.injector
        connectors_storage = injector.connectors_storage
        kafka_producer = injector.kafka_producer
        db_consumer = NewsKafkaDatabaseConsumer(conf, loop, connectors_storage)
        cache_consumer = NewsKafkaCacheConsumer(conf, self.news_conf, loop,
                                                connectors_storage,
                                                injector.redis_client)
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
