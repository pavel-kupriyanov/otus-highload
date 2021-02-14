from typing import Dict

from .db import BaseDatabaseConnector, get_connector
from ..settings import DatabaseSettings


class ConnectorsStorage:

    def __init__(self):
        self._connectors: Dict[str, BaseDatabaseConnector] = {}

    async def create_connector(self, conf: DatabaseSettings) \
            -> BaseDatabaseConnector:
        connector = await get_connector(conf)
        self._connectors[conf.json()] = connector
        return connector

    async def get_connector(self, conf: DatabaseSettings) \
            -> BaseDatabaseConnector:
        connector = self._connectors.get(conf.json())
        if connector is None:
            return await self.create_connector(conf)
        return connector
