from datetime import datetime
from typing import List

from ..crud import CRUDManager
from ..queries import AccessTokenQueries
from ..models import AccessToken, TIMESTAMP_FORMAT


class AccessTokenManager(CRUDManager):
    model = AccessToken

    async def create(self, value: str, user_id: int, expired_at: datetime) \
            -> AccessToken:
        params = (value, user_id, expired_at.strftime(TIMESTAMP_FORMAT))
        return await self._create(params)

    async def update(self, token_id: int, new_expired_at: datetime) \
            -> AccessToken:
        params = (new_expired_at.strftime(TIMESTAMP_FORMAT), token_id)
        return await self._update(token_id, params,
                                  AccessTokenQueries.UPDATE_TOKEN)

    async def list_user_active(self, user_id: int) -> List[AccessToken]:
        query = AccessTokenQueries.GET_USER_ACTIVE_TOKENS
        return await self._list((user_id,), query)

    async def get_by_value(self, value: str) -> AccessToken:
        tokens = await self.execute(AccessTokenQueries.GET_TOKEN_BY_VALUE,
                                    (value,))
        return AccessToken.from_db(tokens[0])
