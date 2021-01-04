from fastapi import Depends

from social_network.db import (
    get_connector,
    get_user_manager,
    BaseDatabaseConnector,
    UserManager,

)


def get_user_manager_depends(
        connector: BaseDatabaseConnector = Depends(get_connector)
) -> UserManager:
    return get_user_manager(connector)
