from collections import namedtuple
from typing import Optional, List
from functools import lru_cache

from pydantic import (
    EmailStr,
    SecretStr
)

from social_network.settings import settings

from ..base import BaseManager, BaseModel
from ..db import BaseDatabaseConnector, DatabaseError
from ..queries import UserQueries


# TODO: additional user info
class UserModel(BaseModel):
    _parsing_tuple = namedtuple('_', 'id, first_name, last_name')

    first_name: str
    last_name: Optional[str]


class AuthUserModel(UserModel):
    _parsing_tuple = namedtuple('_',
                                'id, email, password, first_name, last_name,'
                                'salt')

    email: EmailStr
    password: SecretStr
    salt: SecretStr


class UserManager(BaseManager):
    fields = ('id', 'email', 'password', 'first_name', 'last_name', 'salt')

    async def create(self, email: EmailStr, hashed_password: str, salt: str,
                     first_name: str, last_name: Optional[str] = None) \
            -> AuthUserModel:
        params = (email, hashed_password, salt, first_name, last_name)
        id = await self.execute(UserQueries.CREATE_USER, params,
                                last_row_id=True)
        return AuthUserModel(
            id=id,
            email=email,
            password=hashed_password,
            salt=salt,
            first_name=first_name,
            last_name=last_name
        )

    async def is_email_already_used(self, email: EmailStr) -> bool:
        results = await self.execute(UserQueries.GET_USER, (email, None))
        return bool(results)

    async def get_auth_user(self, id: Optional[int] = None,
                            email: Optional[EmailStr] = None) -> AuthUserModel:
        users = await self.execute(UserQueries.GET_AUTH_USER,
                                   (email, id))
        if not users:
            raise DatabaseError(f'User {email or id} not found.')
        return AuthUserModel.from_db(users[0])

    async def list(self, search='', order_by='last_name', order='ASC',
                   limit=settings.MAX_USERS_ON_PAGE, offset=0) \
            -> List[UserModel]:
        params = (search, search)
        query = self._add_order(UserQueries.GET_USERS, order_by, order)
        query = self._add_limit(query, limit, offset)
        results = await self.execute(query, params)
        return [UserModel.from_db(raw_user) for raw_user in results]


@lru_cache(1)
def get_user_manager(connector: BaseDatabaseConnector) -> UserManager:
    return UserManager(connector)
