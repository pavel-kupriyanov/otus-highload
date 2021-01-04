from datetime import datetime
from collections import namedtuple
from functools import lru_cache
from typing import List, Type

from ..base import BaseModel, M
from ..db import BaseDatabaseConnector
from ..queries import AccessTokenQueries

from .crud import BaseCRUDManager, CRUD

Timestamp = float  # Alias
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class AccessTokenModel(BaseModel):
    value: str
    user_id: int
    expired_at: Timestamp

    _parsing_tuple = namedtuple('_', 'id, value, user_id, expired_at')

    @classmethod
    def from_db(cls: Type[M], tpl: tuple) -> M:
        raw = cls._parsing_tuple(*tpl)._asdict()
        expired_at = raw['expired_at']
        if isinstance(expired_at, str):
            expired_at = datetime.strptime(expired_at, TIMESTAMP_FORMAT)
        if isinstance(expired_at, datetime):
            raw['expired_at'] = expired_at.timestamp()
        return cls(**raw)


class AccessTokenManager(BaseCRUDManager):
    model = AccessTokenModel
    queries = {
        CRUD.CREATE: AccessTokenQueries.CREATE_TOKEN,
        CRUD.UPDATE: AccessTokenQueries.UPDATE_TOKEN,
        CRUD.RETRIEVE: AccessTokenQueries.GET_TOKEN,
        CRUD.LIST: AccessTokenQueries.GET_USER_ACTIVE_TOKENS,
        CRUD.DELETE: AccessTokenQueries.DELETE_TOKEN,
    }

    async def create(self, value: str, user_id: int, expired_at: datetime) \
            -> AccessTokenModel:
        params = (value, user_id, expired_at.strftime(TIMESTAMP_FORMAT))
        return await self._create(params)

    async def update(self, token_id: int, new_expired_at: datetime) \
            -> AccessTokenModel:
        params = (new_expired_at.strftime(TIMESTAMP_FORMAT), token_id)
        return await self._update(token_id, params)

    async def list_user_active(self, user_id: int) -> List[AccessTokenModel]:
        return await self._list((user_id,))

    async def get(self, id: int) -> AccessTokenModel:
        return await self._get(id)

    async def _delete(self, id: int):
        await self._delete(id)


@lru_cache(1)
def get_access_token_manager(connector: BaseDatabaseConnector) \
        -> AccessTokenManager:
    return AccessTokenManager(connector)
