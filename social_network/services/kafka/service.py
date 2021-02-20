from asyncio import AbstractEventLoop
from typing import List, Type

from social_network.settings import KafkaSettings

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
                 loop: AbstractEventLoop,
                 injector: DependencyInjector):
        self.conf = conf
        self.loop = loop
        self.injector = injector
        self.consumers = []

    def init_consumers(self) -> List[BaseKafkaConsumer]:
        conf, loop = self.conf, self.loop
        connectors_storage = self.injector.connectors_storage
        kafka_producer = self.injector.kafka_producer
        db_consumer = NewsKafkaDatabaseConsumer(conf, loop, connectors_storage)
        cache_consumer = NewsKafkaCacheConsumer(conf, loop)
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
