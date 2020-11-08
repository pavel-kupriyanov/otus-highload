import asyncio

from social_network.db.operations import (
    database,
    UserManager
)

manager = UserManager(database)


async def main():
    u = await manager.get_users()
    print(u)
    await manager.db.close()


asyncio.run(main())
