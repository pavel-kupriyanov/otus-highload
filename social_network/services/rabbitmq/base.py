from asyncio import get_running_loop

from aio_pika import Connection, Channel, connect_robust

from social_network.settings import RabbitMQSettings

from ..base import BaseService


class BaseRabbitMQ(BaseService):
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

    async def close(self):
        await self.channel.close()
        await self.connection.close()
