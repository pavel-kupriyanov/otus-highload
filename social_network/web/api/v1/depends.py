from typing import Optional

from fastapi import (
    Header,
    Depends,
    HTTPException
)

# TODO: split imports from db
from social_network.db import (
    get_connector,
    get_auth_user_manager,
    BaseDatabaseConnector,
    AuthUserManager,
    AccessTokenManager,
    FriendRequestManager,
    UserManager,
    FriendshipManager,
    get_access_token_manager,
    get_friend_request_manager,
    get_user_manager,
    get_friendship_manager,
    DatabaseError
)

from social_network.settings import settings


def get_connector_depends():
    return get_connector(settings)


def get_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends)
) -> UserManager:
    return get_user_manager(connector)


def get_auth_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends)
) -> AuthUserManager:
    return get_auth_user_manager(connector)


def get_access_token_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends)
) -> AccessTokenManager:
    return get_access_token_manager(connector)


def get_friend_request_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends)
) -> FriendRequestManager:
    return get_friend_request_manager(connector)


def get_friendship_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector_depends)
) -> FriendshipManager:
    return get_friendship_manager(connector)


async def get_user_id(x_auth_token: Optional[str] = Header(...),
                      access_token_manager: AccessTokenManager = Depends(
                          get_access_token_manager_depends),
                      ) -> Optional[int]:
    if x_auth_token is None:
        return None
    try:
        access_token = await access_token_manager.get_by_value(x_auth_token)
    except DatabaseError:
        raise HTTPException(status_code=401, detail='Invalid token header')
    # TODO: expired check
    return access_token.user_id
