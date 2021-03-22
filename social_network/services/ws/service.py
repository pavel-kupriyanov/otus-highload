import asyncio
from typing import Dict, List
from itertools import chain
from uuid import uuid4

from fastapi import WebSocket

from social_network.settings import RabbitMQSettings

from ..rabbitmq import FeedConsumer
from ..base import BaseService

DATA = {
    "author_id": 1,
    "type": "ADDED_POST",
    "payload": {
        "author": {
            "id": 1,
            "first_name": "sender",
            "last_name": "sender"
        },
        "text": "Hello world"
    },
    "created": 1613736977.09478,
    "populated": True,
    "stored": True
}


class BaseWebSocketService(BaseService):
    sockets: Dict[int, List[WebSocket]]

    def __init__(self):
        self.sockets = {}
        self.task = None

    async def add(self, user_id: int, ws: WebSocket):
        if user_id not in self.sockets:
            self.sockets[user_id] = [ws]
        else:
            self.sockets[user_id].append(ws)

    async def remove(self, user_id: int, ws: WebSocket):
        self.sockets[user_id].remove(ws)

    async def process(self):
        raise NotImplemented

    async def start(self):
        self.task = asyncio.create_task(self.process())

    async def close(self):
        self.task.cancel()
        for ws in list(*self.sockets.values()):
            await ws.close()


class FeedWebSocketService(BaseWebSocketService):
    consumers: Dict[int, FeedConsumer]

    def __init__(self, rabbit_conf: RabbitMQSettings):
        super().__init__()
        self.rabbit_conf = rabbit_conf
        self.consumers = {}

    async def callback(self, data: dict, user_id: int):
        for ws in self.sockets[user_id]:
            await ws.send_json(data)

    async def add(self, user_id: int, ws: WebSocket):
        await super().add(user_id, ws)
        if user_id not in self.consumers.keys():
            await self.add_consumer(user_id)

    async def remove(self, user_id: int, ws: WebSocket):
        await super().remove(user_id, ws)
        if not len(self.sockets[user_id]):
            await self.remove_consumer(user_id)

    async def add_consumer(self, user_id: int):
        async def wrapper(data: dict):
            return await self.callback(data, user_id)

        consumer = FeedConsumer(
            self.rabbit_conf,
            callback=wrapper,
            key=str(user_id)
        )
        await consumer.start()
        self.consumers[user_id] = consumer

    async def remove_consumer(self, user_id: int):
        await self.consumers[user_id].close()
        del self.consumers[user_id]

    async def process(self):
        while True:
            await asyncio.sleep(10000000000)
