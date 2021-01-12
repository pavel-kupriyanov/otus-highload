from enum import Enum


class UserQueries(str, Enum):
    # TODO: find by city
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

    GET_USER_BY_EMAIL = '''
        SELECT id, email, password, salt, age, first_name, last_name, city, gender
        FROM users WHERE email = %s
    '''


class AccessTokenQueries(str, Enum):
    GET_USER_ACTIVE_TOKENS = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE user_id = %s and expired_at > NOW()
    '''

    UPDATE_TOKEN = '''
        UPDATE access_tokens
        SET expired_at = %s
        WHERE id = %s
    '''

    GET_TOKEN_BY_VALUE = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE value = %s
    '''


class FriendRequestQueries(str, Enum):
    UPDATE_FRIEND_REQUEST = '''
        UPDATE friend_requests
        SET status = %s
        WHERE id = %s
    '''

    GET_FRIEND_REQUESTS = '''
        SELECT (id, from_user, to_user, status) FROM friend_requests
        WHERE from_user = %s OR to_user = %s
    '''

    GET_NON_STATUS_FRIEND_REQUESTS = '''
        SELECT (id, from_user, to_user, status) FROM friend_requests
        WHERE (from_user = %s OR to_user = %s) AND status != %s
    '''

    GET_FRIEND_REQUEST_BY_USERS = '''
    SELECT (id, from_user, to_user, status) FROM friend_requests
    WHERE from_user = %s AND to_user = %s
    '''


class FriendshipQueries(str, Enum):
    GET_FRIENDSHIP = '''
        SELECT id, user_id, friend_id FROM friendships
        WHERE user_id = %s AND friend_id = %s
    '''


class HobbyQueries(str, Enum):
    GET_HOBBIES = '''
         SELECT id, name FROM hobbies
         WHERE (UPPER(name) LIKE UPPER(CONCAT('%%', %s, '%%')))
    '''


class UserHobbyQueries(str, Enum):
    DROP_USER_HOBBY = '''
        DELETE FROM users_hobbies_mtm
        WHERE user_id = %s AND hobby_id = %s;
    '''

    GET_HOBBIES_FOR_USERS = '''
        SELECT user_id, h.id, h.name from users_hobbies_mtm
        JOIN hobbies h on h.id = users_hobbies_mtm.hobby_id
        WHERE user_id IN %s
        ORDER BY user_id;
    '''
