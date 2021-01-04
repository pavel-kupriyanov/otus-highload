from enum import Enum


class UserQueries(str, Enum):
    CREATE_USER = '''
        INSERT INTO users(email, password, salt, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s);
        SELECT LAST_INSERT_ID()
    '''

    GET_USER = '''
        SELECT id, first_name, last_name FROM users
        WHERE email = %s OR id = %s
        LIMIT 1
    '''

    GET_USERS = '''
        SELECT id, first_name, last_name FROM users
        WHERE 
        (first_name LIKE CONCAT('%%', %s, '%%')) OR 
        (last_name LIKE CONCAT('%%', %s, '%%'))
    '''

    GET_AUTH_USER = '''
        SELECT id, email, password, first_name, last_name, salt FROM users
        WHERE email = %s OR users.id = %s
        LIMIT 1
    '''


class AccessTokenQueries(str, Enum):
    CREATE_TOKEN = '''
        INSERT INTO access_tokens(value, user_id, expired_at)
        VALUES (%s, %s, %s);
        SELECT LAST_INSERT_ID()
    '''

    GET_USER_ACTIVE_TOKENS = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE user_id = %s and expired_at > NOW()
    '''

    UPDATE_TOKEN = '''
        UPDATE access_tokens
        SET expired_at = %s
        WHERE id = %s
    '''

    GET_TOKEN = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE id = %s OR value = %s
        LIMIT 1
    '''


class FriendRequestQueries(str, Enum):
    CREATE_FRIEND_REQUEST = '''
        INSERT INTO friend_requests(from_user, to_user, status)
        VALUES (%s, %s, %s);
        SELECT LAST_INSERT_ID()
    '''

    UPDATE_FRIEND_REQUEST = '''
        UPDATE friend_requests
        SET status = %s
        WHERE id = %s
    '''

    DROP_FRIEND_REQUEST = '''
        DELETE FROM friend_requests
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

    GET_FRIEND_REQUEST = '''
    SELECT (id, from_user, to_user, status) FROM friend_requests
    WHERE id = %s
    LIMIT 1
    '''
