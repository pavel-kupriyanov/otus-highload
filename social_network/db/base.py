from typing import (
    Tuple,
    Any,
    Optional,
    Iterable,
    TypeVar,
    Type,
)
from collections import namedtuple

from pydantic import BaseModel as PydanticBaseModel

from aiomysql import DatabaseError as RawDatabaseError

from social_network.settings import Settings, settings

from .db import (
    BaseDatabaseConnector,
    DatabaseResponse
)
from .exceptions import DatabaseError

M = TypeVar('M', bound='BaseModel', covariant=True)


class BaseModel(PydanticBaseModel):
    _table_name: str
    _fields: Tuple[Any, ...]

    id: int

    @classmethod
    def from_db(cls: Type[M], tpl: tuple) -> M:
        parsing_tuple = namedtuple('_', cls._fields)
        fields = parsing_tuple(*tpl)._asdict()
        return cls(**fields)


class BaseManager:
    model: M

    def __init__(self, db: BaseDatabaseConnector,
                 conf: Settings = settings):
        self.db = db
        self.conf = conf

    async def execute(self,
                      query: str,
                      params: Optional[Iterable[Any]] = None,
                      last_row_id=False,
                      raise_if_empty=True,
                      execute_many=False) -> DatabaseResponse:
        try:
            return await self.db.make_query(query, params,
                                            last_row_id=last_row_id,
                                            raise_if_empty=raise_if_empty,
                                            execute_many=execute_many)
        except RawDatabaseError as e:
            raise DatabaseError(e.args) from e
