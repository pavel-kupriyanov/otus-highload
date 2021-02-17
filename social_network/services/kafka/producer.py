from zlib import crc32

from aiokafka import AIOKafkaProducer

from social_network.settings import KafkaSettings

from ..base import BaseService


# TODO: partitions
class KafkaProducer(BaseService):
    producer: AIOKafkaProducer

    def __init__(self, conf: KafkaSettings):
        self.conf = conf

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f'{self.conf.HOST}:{self.conf.PORT}'
        )
        await self.producer.start()

    async def close(self):
        await self.producer.stop()

    async def choose_partition(self, key: str) -> int:
        return crc32(key.encode()) % self.conf.PARTITIONS

    async def send(self, data: str, key: str):
        await self.producer.send(
            self.conf.TOPIC_NAME,
            data.encode(),
            partition=self.choose_partition(key)
        )
