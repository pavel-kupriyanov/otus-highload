from typing import Optional
from functools import lru_cache

from fastapi import (
    Header,
    Depends,
    HTTPException
)

# TODO: split imports from db
from social_network.db import (
    get_connector,
    BaseDatabaseConnector,
    AuthUserManager,
    AccessTokenManager,
    FriendRequestManager,
    UserManager,
    FriendshipManager,
    RowsNotFoundError,
    HobbyManager,
    UsersHobbyManager,

)

from social_network.settings import settings, Settings


def get_connector_depends():
    return get_connector(settings)


def get_settings_depends():
    return settings


@lru_cache(1)
def get_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> UserManager:
    return UserManager(connector, conf)


@lru_cache(1)
def get_auth_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> AuthUserManager:
    return AuthUserManager(connector, conf)


@lru_cache(1)
def get_access_token_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> AccessTokenManager:
    return AccessTokenManager(connector, conf)


@lru_cache(1)
def get_friend_request_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> FriendRequestManager:
    return FriendRequestManager(connector, conf)


@lru_cache(1)
def get_friendship_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> FriendshipManager:
    return FriendshipManager(connector, conf)


@lru_cache(1)
def get_hobby_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> HobbyManager:
    return HobbyManager(connector, conf)


@lru_cache(1)
def get_user_hobby_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends),
        conf: Settings = Depends(get_settings_depends)
) -> UsersHobbyManager:
    return UsersHobbyManager(connector, conf)


async def get_user_id(x_auth_token: Optional[str] = Header(None),
                      access_token_manager: AccessTokenManager = Depends(
                          get_access_token_manager_depends),
                      ) -> Optional[int]:
    if x_auth_token is None:
        return None
    try:
        access_token = await access_token_manager.get_by_value(x_auth_token)
    except RowsNotFoundError:
        raise HTTPException(status_code=401, detail='Invalid token header')
    # TODO: expired check
    return access_token.user_id
