import asyncio

from social_network.db.operations import (
    get_connector,
    AuthUserManager
)

manager = AuthUserManager(get_connector())


async def main():
    u = await manager.get_auth_user(id=25, email='kupriyanov2609@gmail.com')
    print(u)
    await manager.db.close()


asyncio.run(main())
