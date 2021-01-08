from fastapi import HTTPException

from functools import wraps


def authorize_only(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if getattr(self, 'user', None) is None:
            raise HTTPException(401, detail='Authorized user only.')
        return await func(self, *args, **kwargs)

    return wrapper
