from typing import List

from social_network.settings import settings

from ..crud import CRUDManager
from ..models import User

GET_USERS = '''
    SELECT id, first_name, last_name, age, city, gender FROM users
    WHERE 
    (first_name LIKE CONCAT('%%', %s, '%%')) AND 
    (last_name LIKE CONCAT('%%', %s, '%%'))
'''

GET_FRIENDS = '''
    SELECT DISTINCT users.id, first_name, last_name, age, city, gender FROM users
    JOIN friendships f on users.id = f.user_id
    WHERE 
    (UPPER(first_name) LIKE UPPER(CONCAT('%%', %s, '%%'))) AND 
    (UPPER(last_name) LIKE UPPER(CONCAT('%%', %s, '%%'))) AND
    (f.friend_id = %s)
'''


class UserManager(CRUDManager):
    model = User
    queries = {}

    async def list(self,
                   first_name='',
                   last_name='',
                   friend_id: int = None,
                   order_by='last_name',
                   order='ASC',
                   limit=settings.BASE_PAGE_LIMIT,
                   offset=0) -> List[User]:
        params = [first_name, last_name]
        query = GET_USERS
        if friend_id:
            params.append(friend_id)
            query = GET_FRIENDS
        return await self._list(tuple(params),
                                query=query,
                                order_by=order_by, order=order,
                                limit=limit, offset=offset)
