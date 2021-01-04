from social_network.settings.base import (
    BaseSettings,
    UvicornSettings,
    DatabaseSettings,
)

CONFIG_PATH = 'settings/settings.json'


class Settings(BaseSettings):
    DEBUG = True
    UVICORN = UvicornSettings()
    DATABASE = DatabaseSettings(PASSWORD='password', NAME='otus_highload')
    TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 7
    MAX_USERS_ON_PAGE = 100


settings = Settings.from_json(CONFIG_PATH)
