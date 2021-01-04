from collections import namedtuple
from typing import Optional
from functools import lru_cache

from pydantic import (
    EmailStr,
    SecretStr
)

from ..db import BaseDatabaseConnector, DatabaseError
from ..queries import UserQueries

from .crud import BaseCRUDManager, CRUD
from .users import UserModel


class AuthUserModel(UserModel):
    _parsing_tuple = namedtuple('_',
                                'id, email, password, first_name, last_name,'
                                'salt')

    email: EmailStr
    password: SecretStr
    salt: SecretStr


class AuthUserManager(BaseCRUDManager):
    fields = ('id', 'email', 'password', 'first_name', 'last_name', 'salt')
    model = AuthUserModel
    queries = {
        CRUD.CREATE: UserQueries.CREATE_USER,
        CRUD.RETRIEVE: UserQueries.GET_AUTH_USER
    }

    async def create(self, email: EmailStr, hashed_password: str, salt: str,
                     first_name: str, last_name: Optional[str] = None) \
            -> AuthUserModel:
        params = (email, hashed_password, salt, first_name, last_name)
        return await self._create(params)

    async def get(self, id: Optional[int] = None,
                  email: Optional[EmailStr] = None) -> AuthUserModel:
        users = await self.execute(UserQueries.GET_USER_BY_EMAIL_OR_ID,
                                   (email, id))
        if not users:
            raise DatabaseError(f'User {email or id} not found.')
        return AuthUserModel.from_db(users[0])

    async def is_email_already_used(self, email: EmailStr) -> bool:
        try:
            await self.get(None, email)
        except DatabaseError:
            return False
        return True


@lru_cache(1)
def get_auth_user_manager(connector: BaseDatabaseConnector) -> AuthUserManager:
    return AuthUserManager(connector)
