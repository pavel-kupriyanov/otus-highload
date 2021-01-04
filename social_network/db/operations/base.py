from typing import (
    Tuple,
    Any,
    Optional,
    Iterable,
    TypeVar,
    Type
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
    _parsing_tuple: Type[namedtuple]

    id: int

    @classmethod
    def from_db(cls: Type[M], tpl: tuple) -> M:
        return cls(**cls._parsing_tuple(*tpl)._asdict())


class BaseManager:

    def __init__(self, db: BaseDatabaseConnector):
        self.db = db

    async def execute(self,
                      query: str,
                      params: Optional[Iterable[Any]] = None,
                      last_row_id=False
                      ) -> DatabaseResponse:
        try:
            return await self.db.make_query(query, params,
                                            last_row_id=last_row_id)
        except RawDatabaseError as e:
            raise DatabaseError(e.args) from e
