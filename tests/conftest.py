import asyncio
import aiomysql
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic import EmailStr

from social_network.settings import Settings
from social_network.db.migrations.main import migrate
from social_network.db import get_connector, BaseDatabaseConnector
from social_network.web.main import app
from social_network.utils.security import hash_password

CONFIG_PATH = 'settings/settings.json'


class TestUser:
    EMAIL = EmailStr('Harkonnen.v@mail.com')
    FIRST_NAME = 'Vladimir'
    LAST_NAME = 'Harkonnen'
    PASSWORD = 'death_for_atreides!'
    HASHED_PASSWORD, SALT = hash_password(PASSWORD)


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


# noinspection SqlResolve
@pytest.fixture(name='test_user')
async def add_user_in_db(cursor: aiomysql.Cursor) -> TestUser:
    u = TestUser()
    await cursor.execute('''
    INSERT INTO users(email, password, salt, first_name, last_name)
    VALUES (%s, %s, %s, %s, %s );
    ''', (u.EMAIL, u.HASHED_PASSWORD, u.SALT, u.FIRST_NAME, u.LAST_NAME))
    yield u
    await cursor.execute('DELETE FROM users WHERE email = %s;',
                         (u.EMAIL,))


@pytest.fixture(name='drop_users_after_test')
async def drop_users_after_test(cursor: aiomysql.Cursor):
    yield
    await cursor.execute('DELETE FROM users')
