from aiokafka import AIOKafkaProducer

from social_network.settings import KafkaSettings

from .consts import Topic
from ..base import BaseService


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

    async def send(self, data: str, topic: str = Topic.News):
        await self.producer.send(topic, data.encode())
