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

from .db import (
    BaseDatabaseConnector,
    DatabaseError,
    DatabaseResponse
)

M = TypeVar('M', covariant=True)


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

    def __init__(self, db: BaseDatabaseConnector):
        self.db = db

    async def execute(self,
                      query: str,
                      params: Optional[Iterable[Any]] = None,
                      last_row_id=False,
                      raise_if_empty=True) -> DatabaseResponse:
        try:
            return await self.db.make_query(query, params,
                                            last_row_id=last_row_id,
                                            raise_if_empty=raise_if_empty)
        except RawDatabaseError as e:
            raise DatabaseError(e.args) from e

    async def count(self, query: str,
                    params: Optional[Iterable[Any]] = None) -> int:
        try:
            return await self.db.make_query(query, params, only_count=True)
        except RawDatabaseError as e:
            raise DatabaseError(e.args) from e
