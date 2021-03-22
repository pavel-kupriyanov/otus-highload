from json import dumps
from asyncio import get_running_loop

from aio_pika import Connection, Channel, Message, connect_robust

from social_network.settings import RabbitMQSettings

from ..base import BaseService


class RabbitMQPProducer(BaseService):
    connection: Connection
    channel: Channel

    def __init__(self, conf: RabbitMQSettings):
        self.conf = conf

    async def start(self):
        conf = self.conf
        password = conf.PASSWORD.get_secret_value()
        self.connection = await connect_robust(
            f'amqp://{conf.USERNAME}:{password}@{conf.HOST}:{conf.PORT}/',
            loop=get_running_loop()
        )
        self.channel = await self.connection.channel()

    async def send(self, data: dict, routing_key: str):
        await self.channel.default_exchange.publish(
            Message(dumps(data).encode()),
            routing_key=routing_key
        )

    async def close(self):
        await self.channel.close()
        await self.connection.close()
