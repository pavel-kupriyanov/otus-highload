import os.path
from social_network.settings.base import (
    BaseSettings,
    UvicornSettings,
    DatabaseSettings,
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, 'settings/settings.json')


class Settings(BaseSettings):
    DEBUG = True
    UVICORN = UvicornSettings()
    DATABASE = DatabaseSettings(PASSWORD='password', NAME='otus_highload')
    TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 7
    BASE_PAGE_LIMIT = 10000


settings = Settings.from_json(CONFIG_PATH)
