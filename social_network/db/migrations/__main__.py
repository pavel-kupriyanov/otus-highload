# TODO: improve migration tool
import os.path

from yoyo import read_migrations
from yoyo import get_backend

from settings.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


def get_db_str():
    return f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


def main():
    backend = get_backend(get_db_str())
    migrations = read_migrations('/'.join([os.path.dirname(__file__), 'sql']))

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


if __name__ == '__main__':
    main()
