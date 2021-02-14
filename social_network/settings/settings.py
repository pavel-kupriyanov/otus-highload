import os.path

from social_network.settings.base import (
    BaseSettings,
    UvicornSettings,
    DatabaseSettings,
    MasterSlaveDatabaseSettings
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, 'settings/settings.json')


class Settings(BaseSettings):
    DEBUG: bool = True
    UVICORN: UvicornSettings = UvicornSettings()
    DATABASE: MasterSlaveDatabaseSettings = MasterSlaveDatabaseSettings(
        MASTER=DatabaseSettings(
            PASSWORD='password',
            NAME='otus_highload'
        )
    )
    TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 7
    BASE_PAGE_LIMIT = 100

    class Config:
        fields = {
            'DATABASE': {
                'env': 'DB_SETTINGS',
            },
        }


# TODO: different runners for heroku and local
settings = Settings.from_json(CONFIG_PATH)
# Heroku needs ENV VARS for application

# settings = Settings()
