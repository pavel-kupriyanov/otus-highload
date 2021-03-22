from json import dumps

from aio_pika import Message

from .base import BaseRabbitMQ


class RabbitMQProducer(BaseRabbitMQ):

    async def send(self, data: dict, routing_key: str):
        exchange = await self.channel.get_exchange('amq.direct')
        print('send', data)
        await exchange.publish(
            Message(dumps(data).encode()),
            routing_key=routing_key
        )
