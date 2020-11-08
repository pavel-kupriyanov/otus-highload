from collections import namedtuple
from typing import Optional, List

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr
)

from .base import BaseManager

# TODO: maybe move queries into separate file?

USER_CREATE_QUERY = '''
INSERT INTO users(email, password, first_name, last_name)
VALUES (%s, %s, %s, %s);
SELECT LAST_INSERT_ID();;
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
    first_name: str
    last_name: Optional[str]


class UserManager(BaseManager):

    async def create(self, email: EmailStr, hashed_password: str,
                     first_name: str, last_name: Optional[str] = None) \
            -> UserModel:
        params = (email, hashed_password, first_name, last_name)
        id = await self._execute(USER_CREATE_QUERY, params, last_row_id=True)
        return UserModel(
            id=id,
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )

    async def get_users(self) -> List[UserModel]:
        raw_users = await self._execute(USER_SELECT_QUERY)
        return [UserModel(**RawUserModel(*raw_user)._asdict())
                for raw_user in raw_users]
