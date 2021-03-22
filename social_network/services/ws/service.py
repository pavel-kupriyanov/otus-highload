import asyncio
from typing import Dict, List
from itertools import chain
from uuid import uuid4

from fastapi import WebSocket

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

    def add(self, user_id: int, ws: WebSocket):
        if user_id not in self.sockets:
            self.sockets[user_id] = [ws]
        else:
            self.sockets[user_id].append(ws)

    def remove(self, user_id: int, ws: WebSocket):
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

    async def process(self):
        while True:
            await asyncio.sleep(10)
            for ws in list(*self.sockets.values()):
                data = dict(DATA)
                data['id'] = str(uuid4())
                await ws.send_json(data)
