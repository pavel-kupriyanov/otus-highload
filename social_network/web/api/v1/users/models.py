from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from social_network.settings import settings


class Order(str, Enum):
    DESC = 'DESC'
    ASC = 'ASC'


class OrderBy(str, Enum):
    ID = 'id'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'


class UsersPayload(BaseModel):
    first_name: str = ''
    last_name: str = ''
    friends_of: Optional[int]
    order_by: OrderBy = Field(OrderBy.LAST_NAME)
    order: Order = Field(Order.ASC)
    page: int = Field(1, ge=1)
    paginate_by: int = Field(settings.BASE_PAGE_LIMIT,
                             le=settings.BASE_PAGE_LIMIT)
