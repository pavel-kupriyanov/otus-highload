from json import loads
from asyncio import create_task
from typing import Callable, Coroutine

from aio_pika import IncomingMessage

from social_network.settings import RabbitMQSettings

from .base import BaseRabbitMQ

Callback = Callable[[dict], Coroutine]


class BaseRabbitMQConsumer(BaseRabbitMQ):
    prefetch_count = 1000
    callback: Callback
    queue_name: str = 'queue'

    def __init__(self, conf: RabbitMQSettings, callback: Callback, key: str):
        super().__init__(conf)
        self.callback = callback
        self.routing_key = key
        self.task = None

    async def start(self):
        await super().start()
        await self.channel.set_qos(prefetch_count=100)
        exchange = await self.channel.get_exchange('amq.direct')
        queue = await self.channel.declare_queue(self.queue_name)
        await queue.bind(exchange, routing_key=self.routing_key)
        self.task = create_task(queue.consume(self.process_message))

    async def close(self):
        await super().close()
        self.task.cancel()

    async def process_message(self, message: IncomingMessage):
        async with message.process():
            print('received', message.body)
            await self.callback(loads(message.body.decode()))


class FeedConsumer(BaseRabbitMQConsumer):
    queue_name: str = 'feed'
