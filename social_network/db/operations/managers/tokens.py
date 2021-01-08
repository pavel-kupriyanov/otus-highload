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


class AccessToken(BaseModel):
    _table_name = 'access_tokens'
    _fields = ('id', 'value', 'user_id', 'expired_at')

    value: str
    user_id: int
    expired_at: Timestamp

    # TODO: refactor it
    @classmethod
    def from_db(cls: Type[M], tpl: tuple) -> M:
        parsing_tuple = namedtuple('_', cls._fields)
        raw = parsing_tuple(*tpl)._asdict()
        expired_at = raw['expired_at']
        if isinstance(expired_at, str):
            expired_at = datetime.strptime(expired_at, TIMESTAMP_FORMAT)
        if isinstance(expired_at, datetime):
            raw['expired_at'] = expired_at.timestamp()
        return cls(**raw)


class AccessTokenManager(BaseCRUDManager):
    model = AccessToken
    queries = {
        CRUD.UPDATE: AccessTokenQueries.UPDATE_TOKEN,
        CRUD.LIST: AccessTokenQueries.GET_USER_ACTIVE_TOKENS,
    }

    async def create(self, value: str, user_id: int, expired_at: datetime) \
            -> AccessToken:
        params = (value, user_id, expired_at.strftime(TIMESTAMP_FORMAT))
        return await self._create(params)

    async def update(self, token_id: int, new_expired_at: datetime) \
            -> AccessToken:
        params = (new_expired_at.strftime(TIMESTAMP_FORMAT), token_id)
        return await self._update(token_id, params)

    async def list_user_active(self, user_id: int) -> List[AccessToken]:
        return await self._list((user_id,))

    async def get(self, id: int) -> AccessToken:
        return await self._get(id)

    async def get_by_value(self, value: str) -> AccessToken:
        params = (None, value)
        token = await self.execute(AccessTokenQueries.GET_TOKEN_BY_VALUE_OR_ID,
                                   params)
        return AccessToken.from_db(token)

    async def _delete(self, id: int):
        await self._delete(id)


@lru_cache(1)
def get_access_token_manager(connector: BaseDatabaseConnector) \
        -> AccessTokenManager:
    return AccessTokenManager(connector)
