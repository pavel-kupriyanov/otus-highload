from time import sleep

from fastapi.testclient import TestClient

from social_network.db.models import AccessToken, User
from social_network.db.sharding.models import Message

BASE_PATH = '/api/v1/messages/'


def test_create_message(app: TestClient, message_shards, token1: AccessToken,
                        user2: User):
    msg = {'to_user_id': user2.id, 'text': 'Hi!'}
    response = app.post(BASE_PATH, json=msg,
                        headers={'x-auth-token': token1.value})
    assert response.status_code == 201
    assert response.json()['text'] == msg['text']


def test_get_messages(app: TestClient, token1: AccessToken, message_1: Message,
                      user2):
    response = app.get(BASE_PATH,
                       params={'to_user_id': user2.id},
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 200
    msg = response.json()[0]
    assert msg['text'] == message_1.text


def test_get_messages_from_timestamp(app: TestClient, token1: AccessToken,
                                     message_1: Message, user2):
    sleep(2)  # sleep to get pause between 1 and 2 message
    msg = {'to_user_id': user2.id, 'text': 'Hi!'}
    headers = {'x-auth-token': token1.value}
    response = app.post(BASE_PATH, json=msg, headers=headers)
    timestamp = float(response.json()['created'])

    params = {'to_user_id': user2.id}
    response = app.get(BASE_PATH, params=params, headers=headers)
    assert len(response.json()) == 2

    params['after_timestamp'] = timestamp - 1
    response = app.get(BASE_PATH, params=params, headers=headers)
    assert len(response.json()) == 1
    assert response.json()[0]['text'] == msg['text']
