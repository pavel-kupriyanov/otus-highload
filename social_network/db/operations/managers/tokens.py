from datetime import datetime
from collections import namedtuple
from functools import lru_cache
from typing import List, Type

from ..base import BaseManager, BaseModel, M
from ..db import BaseDatabaseConnector
from ..queries import AccessTokenQueries

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


class AccessTokenManager(BaseManager):

    async def create(self, value: str, user_id: int, expired_at: datetime) \
            -> AccessTokenModel:
        params = (value, user_id, expired_at.strftime(TIMESTAMP_FORMAT))
        id = await self.execute(AccessTokenQueries.CREATE_TOKEN, params,
                                last_row_id=True)
        return AccessTokenModel(
            id=id,
            value=value,
            user_id=user_id,
            expired_at=expired_at.timestamp(),
        )

    async def list_active(self, user_id: int) \
            -> List[AccessTokenModel]:
        tokens = await self.execute(AccessTokenQueries.GET_USER_ACTIVE_TOKENS,
                                    (user_id,))
        return [AccessTokenModel.from_db(token) for token in tokens]

    async def update(self, token_id: int, new_expired_at: datetime) \
            -> AccessTokenModel:
        # TODO: session
        params = (new_expired_at.strftime(TIMESTAMP_FORMAT), token_id)
        await self.execute(AccessTokenQueries.UPDATE_TOKEN, params)

        tokens = await self.execute(AccessTokenQueries.GET_TOKEN,
                                    (token_id, None))
        return AccessTokenModel.from_db(tokens[0])


@lru_cache(1)
def get_access_token_manager(connector: BaseDatabaseConnector) \
        -> AccessTokenManager:
    return AccessTokenManager(connector)
