from random import choice
from string import ascii_letters, digits

from fastapi import Depends

from social_network.db import (
    get_connector,
    get_auth_user_manager,
    AuthUserModel,
    BaseDatabaseConnector,
    AuthUserManager,
    AccessTokenManager,
    get_access_token_manager
)

from social_network.utils.security import check_hash


def is_valid_password(user: AuthUserModel, password: str) -> bool:
    user_password = user.password.get_secret_value()
    salt = user.salt.get_secret_value()
    return check_hash(password, user_password, salt)


def generate_token_value(length=255) -> str:
    alphabet = ascii_letters + digits
    return ''.join((choice(alphabet) for _ in range(length)))


def get_auth_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector)
) -> AuthUserManager:
    return get_auth_user_manager(connector)


def get_access_token_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector)
) -> AccessTokenManager:
    return get_access_token_manager(connector)
