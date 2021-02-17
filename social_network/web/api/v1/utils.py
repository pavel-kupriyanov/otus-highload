from enum import Enum
from fastapi import HTTPException

from functools import wraps


class Order(str, Enum):
    DESC = 'DESC'
    ASC = 'ASC'


def authorize_only(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        u_id, u = getattr(self, 'user_id', None), getattr(self, 'user', None)
        if (u_id or u) is None:
            raise HTTPException(401, detail='Authorized user only.')
        return await func(self, *args, **kwargs)

    return wrapper
