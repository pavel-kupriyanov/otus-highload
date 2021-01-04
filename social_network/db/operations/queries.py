from enum import Enum


class UserQueries(str, Enum):
    CREATE_USER = '''
    INSERT INTO users(email, password, salt, first_name, last_name)
    VALUES (%s, %s, %s, %s, %s);
    SELECT LAST_INSERT_ID();
    '''

    GET_USER = '''
        SELECT id, first_name, last_name FROM users
        WHERE email = %s OR id = %s
        LIMIT 1;
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
        LIMIT 1;
    '''


class AccessTokenQueries(str, Enum):
    CREATE_TOKEN = '''
        INSERT INTO access_tokens(value, user_id, expired_at)
        VALUES (%s, %s, %s);
        SELECT LAST_INSERT_ID();
    '''

    GET_USER_ACTIVE_TOKENS = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE user_id = %s and expired_at > NOW()
    '''

    UPDATE_TOKEN = '''
        UPDATE access_tokens
        SET expired_at = %s
        WHERE id = %s;
    '''

    GET_TOKEN = '''
        SELECT id, value, user_id, expired_at FROM access_tokens
        WHERE id = %s OR value = %s
        LIMIT 1;
    '''
