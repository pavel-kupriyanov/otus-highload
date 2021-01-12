import asyncio
from datetime import datetime, timedelta
from typing import Any

import aiomysql
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic import EmailStr

from social_network.settings import Settings
from social_network.db.migrations.main import migrate
from social_network.db.db import (
    get_connector,
    BaseDatabaseConnector
)
from social_network.db.models import (
    AccessToken,
    AuthUser,
    Friendship,
    FriendRequest,
    Hobby,
    UserHobby
)
from social_network.db.managers import (
    AccessTokenManager,
    AuthUserManager,
    FriendRequestManager,
    FriendshipManager,
    HobbiesManager,
    UsersHobbyManager
)
from social_network.web.main import app
from social_network.utils.security import hash_password

CONFIG_PATH = 'settings/settings.json'


class VladimirHarconnen:
    ID: int
    EMAIL = EmailStr('Harkonnen.v@mail.com')
    FIRST_NAME = 'Vladimir'
    LAST_NAME = 'Harkonnen'
    PASSWORD = 'death_for_atreides!'
    HASHED_PASSWORD, SALT = hash_password(PASSWORD)
    AGE = 83
    CITY = 'Arrakis'
    GENDER = 'MALE'


class LetoAtreides:
    ID: int
    EMAIL = EmailStr('Atreides.L@mail.com')
    FIRST_NAME = 'Leto'
    LAST_NAME = 'Atreides'
    PASSWORD = 'death_for_harconnen!'
    HASHED_PASSWORD, SALT = hash_password(PASSWORD)
    AGE = 51
    CITY = 'Arrakis'
    GENDER = 'MALE'


class ShaddamIV:
    ID: int
    EMAIL = EmailStr('Emperor@mail.com')
    FIRST_NAME = 'Shaddam'
    LAST_NAME = 'IV'
    PASSWORD = 'SpiceMustFlow'
    HASHED_PASSWORD, SALT = hash_password(PASSWORD)
    AGE = 68
    CITY = None
    GENDER = None


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Fix for bug https://github.com/pytest-dev/pytest-asyncio/issues/171
pytest_asyncio.plugin.event_loop = event_loop


@pytest.fixture(name='settings', scope='session')
def get_settings() -> Settings:
    return Settings.from_json(CONFIG_PATH)


@pytest.fixture(name='cursor', scope='session')
async def get_cursor(settings) -> aiomysql.Cursor:
    db_conf = settings.DATABASE
    conn = await aiomysql.connect(host=db_conf.HOST,
                                  port=db_conf.PORT,
                                  user=db_conf.USER,
                                  db=db_conf.NAME,
                                  password=db_conf.PASSWORD.get_secret_value(),
                                  autocommit=True)
    async with conn.cursor() as cursor:
        yield cursor


@pytest.fixture(name='db', autouse=True, scope='session')
async def create_test_database(settings: Settings):
    db_conf = settings.DATABASE
    conn = await aiomysql.connect(host=db_conf.HOST,
                                  port=db_conf.PORT,
                                  user=db_conf.USER,
                                  password=db_conf.PASSWORD.get_secret_value(),
                                  autocommit=True)
    cursor = await conn.cursor()
    try:
        await cursor.execute(f"CREATE SCHEMA {db_conf.NAME};")
    except Exception:
        await cursor.execute(f"DROP SCHEMA {db_conf.NAME};")
        await cursor.execute(f"CREATE SCHEMA {db_conf.NAME};")

    migrate(db_conf)
    yield
    await cursor.execute(f"DROP SCHEMA {db_conf.NAME};")


@pytest.fixture(name='db_connector')
def get_db_connector(settings) -> BaseDatabaseConnector:
    return get_connector(settings)


@pytest.fixture(name='app')
async def get_test_client(db_connector) -> TestClient:
    app.dependency_overrides['db_connector'] = lambda: db_connector
    yield TestClient(app)
    app.dependency_overrides = {}


@pytest.fixture(name='user1')
async def add_user_in_db1(db_connector, settings,
                          cursor: aiomysql.Cursor) -> AuthUser:
    yield await add_user_in_db(db_connector, settings, VladimirHarconnen)
    await cursor.execute('DELETE FROM users WHERE email = %s;',
                         (VladimirHarconnen.EMAIL,))


@pytest.fixture(name='user2')
async def add_user_in_db2(db_connector, settings,
                          cursor: aiomysql.Cursor) -> AuthUser:
    yield await add_user_in_db(db_connector, settings, LetoAtreides)
    await cursor.execute('DELETE FROM users WHERE email = %s;',
                         (LetoAtreides.EMAIL,))


@pytest.fixture(name='user3')
async def add_user_in_db3(db_connector, settings,
                          cursor: aiomysql.Cursor) -> AuthUser:
    yield await add_user_in_db(db_connector, settings, ShaddamIV)
    await cursor.execute('DELETE FROM users WHERE email = %s;',
                         (ShaddamIV.EMAIL,))


@pytest.fixture(name='token1')
async def get_token_for_user1(user1, db_connector, settings) -> AccessToken:
    return await add_token_in_db(db_connector, settings, user1.id)


@pytest.fixture(name='token2')
async def get_token_for_user2(user2, db_connector, settings) -> AccessToken:
    return await add_token_in_db(db_connector, settings, user2.id)


@pytest.fixture(name='token3')
async def get_token_for_user3(user3, db_connector, settings) -> AccessToken:
    return await add_token_in_db(db_connector, settings, user3.id)


@pytest.fixture(name='friend_request')
async def get_friend_request(db_connector, settings, user1, user2, cursor) \
        -> FriendRequest:
    return await add_friend_request_in_db(db_connector, settings, user1.id,
                                          user2.id)


@pytest.fixture(name='friendship')
async def get_friendship(db_connector, settings, user1, user2, cursor) \
        -> Friendship:
    return await add_friendship_in_db(db_connector, settings, user1.id,
                                      user2.id)


@pytest.fixture(name='hobby')
async def get_hobby(db_connector, settings, cursor: aiomysql.Cursor) -> Hobby:
    yield await add_hobby_in_db(db_connector, settings, 'War')
    await cursor.execute('DELETE FROM hobbies;')


@pytest.fixture(name='user_hobby')
async def get_user_hobby(db_connector, settings, user1, hobby,
                         cursor: aiomysql.Cursor) \
        -> UserHobby:
    yield await add_user_hobby_in_db(db_connector, settings, user1.id, hobby.id)
    await cursor.execute('DELETE FROM users_hobbies_mtm;')


@pytest.fixture(name='drop_users_after_test')
async def drop_users_after_test(cursor: aiomysql.Cursor):
    yield
    await cursor.execute('DELETE FROM users')


async def add_user_in_db(db_connector, settings, user_data: Any) -> AuthUser:
    manager = AuthUserManager(db_connector, settings)
    user = await manager.create(email=user_data.EMAIL,
                                age=user_data.AGE,
                                hashed_password=user_data.HASHED_PASSWORD,
                                salt=user_data.SALT,
                                first_name=user_data.FIRST_NAME,
                                last_name=user_data.LAST_NAME,
                                city=user_data.CITY,
                                gender=user_data.GENDER)
    user.password = user_data.PASSWORD
    return user


async def add_token_in_db(db_connector, settings, user_id):
    manager = AccessTokenManager(db_connector, settings)
    expired_at = datetime.now() + timedelta(
        seconds=settings.TOKEN_EXPIRATION_TIME
    )
    return await manager.create('foobar', user_id, expired_at)


async def add_friend_request_in_db(db_connector, settings, from_user_id,
                                   to_user_id) -> FriendRequest:
    manager = FriendRequestManager(db_connector, settings)
    return await manager.create(from_user_id, to_user_id)


async def add_friendship_in_db(db_connector, settings, user_id, friend_id) \
        -> Friendship:
    manager = FriendshipManager(db_connector, settings)
    return await manager.create(user_id, friend_id)


async def add_hobby_in_db(db_connector, settings, hobby_name: str) -> Hobby:
    manager = HobbiesManager(db_connector, settings)
    return await manager.create(hobby_name)


async def add_user_hobby_in_db(db_connector, settings, user_id, hobby_id) \
        -> UserHobby:
    manager = UsersHobbyManager(db_connector, settings)
    return await manager.create(user_id, hobby_id)
