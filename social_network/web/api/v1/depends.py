from typing import Optional, Type, TypeVar
from functools import lru_cache
from datetime import datetime

from fastapi import (
    Header,
    Depends,
    Request,
    HTTPException
)
from social_network.db.models import User
from social_network.db.managers import (
    AuthUserManager,
    AccessTokenManager,
    FriendRequestManager,
    UserManager,
    FriendshipManager,
    HobbiesManager,
    UsersHobbyManager,
    NewsManager,
)
from social_network.db.sharding.managers import MessagesManager

from social_network.db.connectors_storage import BaseConnectorStorage
from social_network.db.exceptions import RowsNotFoundError
from social_network.settings import settings, Settings

M = TypeVar('M')


class DependencyInjector:

    def __init__(self, connector_storage: BaseConnectorStorage, conf: Settings):
        self.connector_storage = connector_storage
        self.conf = conf

    def get_manager(self, cls: Type[M]) -> M:
        return cls(self.connector_storage, self.conf)


@lru_cache(1)
def get_settings_depends():
    return settings


def get_connectors_storage_storage(request: Request):
    return request.app.state.connectors_storage


def get_kafka_producer(request: Request):
    return request.app.state.kafka_producer


def get_injector(
        connector_storage: BaseConnectorStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> DependencyInjector:
    return DependencyInjector(connector_storage, conf)


@lru_cache(1)
def get_user_manager(injector=Depends(get_injector)) -> UserManager:
    return injector.get_manager(UserManager)


@lru_cache(1)
def get_auth_user_manager(injector=Depends(get_injector)) -> AuthUserManager:
    return injector.get_manager(AuthUserManager)


@lru_cache(1)
def get_access_token_manager(injector=Depends(get_injector)) \
        -> AccessTokenManager:
    return injector.get_manager(AccessTokenManager)


@lru_cache(1)
def get_friend_request_manager(injector=Depends(get_injector)) \
        -> FriendRequestManager:
    return injector.get_manager(FriendRequestManager)


@lru_cache(1)
def get_friendship_manager(injector=Depends(get_injector)) -> FriendshipManager:
    return injector.get_manager(FriendshipManager)


@lru_cache(1)
def get_hobby_manager(injector=Depends(get_injector)) -> HobbiesManager:
    return injector.get_manager(HobbiesManager)


@lru_cache(1)
def get_user_hobby_manager(injector=Depends(get_injector)) -> UsersHobbyManager:
    return injector.get_manager(UsersHobbyManager)


@lru_cache(1)
def get_messages_manager(injector=Depends(get_injector)) -> MessagesManager:
    return injector.get_manager(MessagesManager)


@lru_cache(1)
def get_news_manager(injector=Depends(get_injector)) -> MessagesManager:
    return injector.get_manager(NewsManager)


async def get_user_id(
        x_auth_token: Optional[str] = Header(None),
        access_token_manager: AccessTokenManager = Depends(
            get_access_token_manager),
) -> Optional[int]:
    if x_auth_token is None:
        return None
    try:
        access_token = await access_token_manager.get_by_value(x_auth_token)
    except RowsNotFoundError:
        raise HTTPException(status_code=401, detail='Invalid token header')
    if datetime.fromtimestamp(access_token.expired_at) < datetime.now():
        raise HTTPException(status_code=400,
                            detail='Expired token, please re-login')
    return access_token.user_id


async def get_user(
        user_id: int = Depends(get_user_id),
        user_manager: UserManager = Depends(get_user_manager)
) -> Optional[User]:
    if user_id is None:
        return None
    return await user_manager.get(user_id)
