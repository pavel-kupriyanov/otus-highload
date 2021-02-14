from enum import Enum
from typing import Type, Optional, List
from collections import namedtuple

from pydantic import (
    Field,
    EmailStr,
    SecretStr
)

from .base import M, BaseModel
from ..settings import DatabaseSettings


class FriendRequestStatus(str, Enum):
    WAITING = 'WAITING'
    DECLINED = 'DECLINED'


class FriendRequest(BaseModel):
    _table_name = 'friend_requests'
    _fields = ('id', 'from_user', 'to_user', 'status')

    from_user: int
    to_user: int
    status: FriendRequestStatus


class Friendship(BaseModel):
    _table_name = 'friendships'
    _fields = ('id', 'user_id', 'friend_id')

    user_id: int
    friend_id: int


class Hobby(BaseModel):
    _table_name = 'hobbies'
    _fields = ('id', 'name')

    name: str


Timestamp = float  # Alias
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class AccessToken(BaseModel):
    _table_name = 'access_tokens'
    _fields = ('id', 'value', 'user_id', 'expired_at')

    value: str
    user_id: int
    expired_at: Timestamp

    @classmethod
    def from_db(cls: Type[M], tpl: tuple) -> M:
        parsing_tuple = namedtuple('_', cls._fields)
        raw = parsing_tuple(*tpl)._asdict()
        raw['expired_at'] = raw['expired_at'].timestamp()
        return cls(**raw)


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class User(BaseModel):
    _table_name = 'users'
    _fields = ('id', 'first_name', 'last_name', 'age', 'city', 'gender')

    first_name: str
    last_name: Optional[str]
    city: Optional[str]
    gender: Optional[Gender]
    age: int = Field(..., ge=1, le=200)
    hobbies: List[Hobby] = Field(default_factory=list)


class AuthUser(User):
    _table_name = 'users'
    _fields = ('id', 'email', 'password', 'salt', 'age', 'first_name',
               'last_name', 'city', 'gender')

    email: EmailStr
    password: SecretStr
    salt: SecretStr


class UserHobby(BaseModel):
    _table_name = 'users_hobbies_mtm'
    _fields = ('id', 'user_id', 'hobby_id')

    user_id: int
    hobby_id: int


class DatabaseInfo(BaseModel):
    _table_name = 'database_info'
    _fields = ('id', 'host', 'port', 'user', 'password', 'name')

    host: str
    port: int
    user: str
    password: SecretStr
    name: str

    def as_settings(self) -> DatabaseSettings:
        return DatabaseSettings(
            HOST=self.host,
            PORT=self.port,
            USER=self.user,
            PASSWORD=self.password.get_secret_value(),
            NAME=self.name
        )


class ShardState(str, Enum):
    READY = 'READY'
    ADDING = 'ADDING'
    DELETING = 'DELETING'
    ERROR = 'ERROR'


class Shard(BaseModel):
    _table_name = 'shards_info'
    _fields = ('id', 'db_info', 'shard_table', 'shard_key', 'state')

    db_info: DatabaseInfo
    shard_table: str
    shard_key: int
    state: ShardState
