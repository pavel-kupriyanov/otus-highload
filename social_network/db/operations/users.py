from collections import namedtuple
from typing import Optional, List
from functools import lru_cache

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr
)

from .base import BaseManager
from .db import BaseDatabaseConnector

# TODO: maybe move queries into separate file?

EMAIL_CHECK_QUERY = '''
    SELECT id FROM users
    WHERE email = %s;
'''

USER_CREATE_QUERY = '''
INSERT INTO users(email, password, salt, first_name, last_name)
VALUES (%s, %s, %s, %s, %s);
SELECT LAST_INSERT_ID();
'''

USER_SELECT_QUERY = '''
    SELECT * FROM users;
'''

RawUserModel = namedtuple('RawUserModel',
                          'id, email, password, first_name, last_name')


class UserModel(BaseModel):
    id: int
    email: EmailStr
    password: SecretStr
    salt: str
    first_name: str
    last_name: Optional[str]


class UserManager(BaseManager):

    async def create(self, email: EmailStr, hashed_password: str, salt: str,
                     first_name: str, last_name: Optional[str] = None) \
            -> UserModel:
        params = (email, hashed_password, salt, first_name, last_name)
        id = await self._execute(USER_CREATE_QUERY, params, last_row_id=True)
        return UserModel(
            id=id,
            email=email,
            password=hashed_password,
            salt=salt,
            first_name=first_name,
            last_name=last_name
        )

    async def is_email_already_used(self, email: EmailStr) -> bool:
        results = await self._execute(EMAIL_CHECK_QUERY, (email,))
        return bool(results)

    async def get_users(self) -> List[UserModel]:
        raw_users = await self._execute(USER_SELECT_QUERY)
        # TODO: rewrite this shit
        return [UserModel(**RawUserModel(*raw_user)._asdict())
                for raw_user in raw_users]


@lru_cache(1)
def get_user_manager(connector: BaseDatabaseConnector) -> UserManager:
    return UserManager(connector)
