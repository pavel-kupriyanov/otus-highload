from typing import Type, TypeVar

from social_network.db.connectors_storage import ConnectorsStorage
from social_network.settings import Settings

from .base import BaseService
from .kafka import KafkaProducer

M = TypeVar('M')


class DependencyInjector(BaseService):
    connectors_storage: ConnectorsStorage
    kafka_producer: KafkaProducer

    def __init__(self, conf: Settings):
        self.conf = conf

    async def start(self):
        self.connectors_storage = await self.get_connectors_storage()
        self.kafka_producer = await self.get_kafka_producer()

    async def close(self):
        await self.kafka_producer.close()

    async def get_connectors_storage(self) -> ConnectorsStorage:
        connectors_storage = ConnectorsStorage()
        await connectors_storage.create_connector(self.conf.DATABASE.MASTER)

        for conf in self.conf.DATABASE.SLAVES:
            await connectors_storage.create_connector(conf)

        return connectors_storage

    async def get_kafka_producer(self) -> KafkaProducer:
        producer = KafkaProducer(self.conf.KAFKA)
        await producer.start()
        return producer

    def get_manager(self, cls: Type[M]) -> M:
        return cls(self.connectors_storage, self.conf)
