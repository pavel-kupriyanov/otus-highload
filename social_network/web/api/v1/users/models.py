from dataclasses import dataclass
from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from social_network.settings import settings


class Order(str, Enum):
    DESC = 'DESC'
    ASC = 'ASC'


class OrderBy(str, Enum):
    ID = 'id'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'


@dataclass
class UsersQueryParams:
    first_name: str = Query('')
    last_name: str = Query('')
    friends_of: Optional[int] = Query(None)
    order_by: OrderBy = Query(OrderBy.FIRST_NAME)
    order: Order = Query(Order.ASC)
    page: int = Query(1, ge=1)
    paginate_by: int = Query(settings.BASE_PAGE_LIMIT,
                             le=settings.BASE_PAGE_LIMIT)
