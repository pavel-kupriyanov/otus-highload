class BaseService:

    async def start(self):
        raise NotImplemented

    async def close(self):
        raise NotImplemented
