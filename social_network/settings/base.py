import os
import json
from copy import deepcopy
from typing import List

from pydantic import (
    BaseModel,
    BaseSettings as PydanticSettings,
    SecretStr
)


class UvicornSettings(BaseModel):
    # TODO: fix module object is not callable
    ASGI_PATH: str = 'web:app'
    HOST: str = '0.0.0.0'
    PORT: int = int(os.getenv('PORT') or 8000)
    WORKERS = 4


class DatabaseSettings(BaseModel):
    DB: str = 'mysql'
    HOST: str = 'localhost'
    PORT: int = 3306
    USER: str = 'root'
    PASSWORD: SecretStr
    NAME: str
    MAX_CONNECTIONS = 1


class MasterSlaveDatabaseSettings(BaseModel):
    MASTER: DatabaseSettings
    SLAVES: List[DatabaseSettings] = []


class BaseSettings(PydanticSettings):
    DEBUG: bool
    UVICORN: UvicornSettings
    DATABASE: MasterSlaveDatabaseSettings

    @classmethod
    def from_json(cls, path):
        with open(path) as fp:
            merged_settings = deep_merge(cls().dict(), json.load(fp))
        return cls.parse_obj(merged_settings)

    def __hash__(self):
        # For lru cache
        return hash(self.json())


def deep_merge(first: dict, second: dict) -> dict:
    res = deepcopy(first)
    for key, value in second.items():
        if key in res and isinstance(res[key], dict) and isinstance(value,
                                                                    dict):
            res[key] = deep_merge(res[key], value)
        else:
            res[key] = value

    return res
