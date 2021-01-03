from collections import namedtuple
from typing import Optional, List
from functools import lru_cache

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr
)

from .base import BaseManager
from .db import BaseDatabaseConnector, DatabaseError
from .queries import UserQueries


class UserModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: Optional[str]

    _raw_user_model = namedtuple('_', 'id, email, first_name, last_name')

    @classmethod
    def from_db(cls, raw_user: tuple) -> 'UserModel':
        return cls(**cls._raw_user_model(*raw_user)._asdict())


class AuthUserModel(UserModel):
    password: SecretStr
    salt: SecretStr

    _raw_user_model = namedtuple('_',
                                 'id, email, password, first_name, last_name,'
                                 'salt')


class UserManager(BaseManager):

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

    async def get_users(self) -> List[AuthUserModel]:
        results = await self.execute(UserQueries.GET_USERS)
        return [AuthUserModel.from_db(raw_user) for raw_user in results]


@lru_cache(1)
def get_user_manager(connector: BaseDatabaseConnector) -> UserManager:
    return UserManager(connector)
