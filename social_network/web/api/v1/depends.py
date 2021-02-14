from typing import Optional
from functools import lru_cache
from datetime import datetime

from fastapi import (
    Header,
    Depends,
    Request,
    HTTPException
)

from social_network.db.managers import (
    AuthUserManager,
    AccessTokenManager,
    FriendRequestManager,
    UserManager,
    FriendshipManager,
    HobbiesManager,
    UsersHobbyManager,
)

from social_network.db.connectors_storage import ConnectorsStorage
from social_network.db.exceptions import RowsNotFoundError
from social_network.settings import settings, Settings


@lru_cache(1)
def get_settings_depends():
    return settings


def get_connectors_storage_storage(request: Request):
    return request.app.state.connectors_storage


# TODO: Remove duplicate dependencies
@lru_cache(1)
def get_user_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> UserManager:
    return UserManager(connector_storage, conf)


@lru_cache(1)
def get_auth_user_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> AuthUserManager:
    return AuthUserManager(connector_storage, conf)


@lru_cache(1)
def get_access_token_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> AccessTokenManager:
    return AccessTokenManager(connector_storage, conf)


@lru_cache(1)
def get_friend_request_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> FriendRequestManager:
    return FriendRequestManager(connector_storage, conf)


@lru_cache(1)
def get_friendship_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> FriendshipManager:
    return FriendshipManager(connector_storage, conf)


@lru_cache(1)
def get_hobby_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> HobbiesManager:
    return HobbiesManager(connector_storage, conf)


@lru_cache(1)
def get_user_hobby_manager(
        connector_storage: ConnectorsStorage = Depends(
            get_connectors_storage_storage
        ),
        conf: Settings = Depends(get_settings_depends)
) -> UsersHobbyManager:
    return UsersHobbyManager(connector_storage, conf)


async def get_user_id(x_auth_token: Optional[str] = Header(None),
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
