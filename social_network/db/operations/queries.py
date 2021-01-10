from enum import Enum


class UserQueries(str, Enum):
    GET_USERS = '''
        SELECT id, first_name, last_name FROM users
        WHERE 
        (first_name LIKE CONCAT('%%', %s, '%%')) AND 
        (last_name LIKE CONCAT('%%', %s, '%%'))
    '''

    GET_FRIENDS = '''
        SELECT DISTINCT users.id, first_name, last_name FROM users
        JOIN friendships f1 on users.id = f1.user_id1
        JOIN friendships f2 on users.id = f2.user_id2
        WHERE 
        (first_name LIKE CONCAT('%%', %s, '%%')) AND 
        (last_name LIKE CONCAT('%%', %s, '%%'))
    '''

    GET_USERS_BY_IDS = '''
        SELECT id, first_name, last_name FROM users
        WHERE id IN %s
    '''

    GET_USER_BY_EMAIL_OR_ID = '''
        SELECT id, email, password, salt, first_name, last_name FROM users
        WHERE email = %s OR users.id = %s
        LIMIT 1
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

    GET_TOKEN_BY_VALUE_OR_ID = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE id = %s OR value = %s
        LIMIT 1
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
    LIMIT 1
    '''


class FriendshipQueries(str, Enum):
    GET_FRIENDSHIP = '''
        SELECT id, user_id, friend_id FROM friendships
        WHERE user_id = %s AND friend_id = %s
    '''
