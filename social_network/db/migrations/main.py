# TODO: improve migration tool
import os

from yoyo import read_migrations
from yoyo import get_backend

from social_network.settings import DatabaseSettings


def get_db_str(s: DatabaseSettings):
    return f'{s.DB}://{s.USER}:{s.PASSWORD.get_secret_value()}' \
           f'@{s.HOST}:{s.PORT}/{s.NAME}'


def migrate(conf: DatabaseSettings):
    backend = get_backend(get_db_str(conf))
    migrations = read_migrations('/'.join([os.path.dirname(__file__), 'sql']))

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
