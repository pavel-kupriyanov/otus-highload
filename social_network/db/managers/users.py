from typing import List, Optional

from social_network.settings import settings

from ..crud import CRUDManager
from ..models import User

GET_USERS = '''
    SELECT id, first_name, last_name, age, city, gender FROM users
    WHERE 
    (first_name LIKE UPPER(CONCAT(%s, '%%')))
     AND 
    (last_name LIKE UPPER(CONCAT(%s, '%%')) OR ISNULL(last_name))
'''

GET_FRIENDS = '''
    SELECT DISTINCT users.id, first_name, last_name, age, city, gender FROM users
    JOIN friendships f on users.id = f.user_id
    WHERE 
    (UPPER(first_name) LIKE UPPER(CONCAT('%%', %s, '%%')))
     AND 
    (UPPER(last_name) LIKE UPPER(CONCAT('%%', %s, '%%')) OR ISNULL(last_name))
     AND
    (f.friend_id = %s)
'''

GET_BY_IDS = '''
    SELECT DISTINCT id, first_name, last_name, age, city, gender FROM users
    WHERE
   (UPPER(first_name) LIKE UPPER(CONCAT('%%', %s, '%%')))
     AND 
    (UPPER(last_name) LIKE UPPER(CONCAT('%%', %s, '%%')) OR ISNULL(last_name))
     AND
    (id IN  %s)
'''


class UserManager(CRUDManager):
    model = User
    queries = {}

    async def list(self,
                   first_name='',
                   last_name='',
                   friend_id: Optional[int] = None,
                   ids: Optional[List[int]] = None,
                   order_by='last_name',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[User]:
        params = [first_name.upper(), last_name.upper()]
        query = GET_USERS
        if friend_id:
            params.append(friend_id)
            query = GET_FRIENDS
        elif ids:
            params.append(ids)
            query = GET_BY_IDS
        return await self._list(tuple(params),
                                query=query,
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)
