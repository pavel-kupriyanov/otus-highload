from fastapi.testclient import TestClient

from social_network.db import AccessToken

BASE_PATH = '/api/v1/users/'


def test_get(app: TestClient, user1, user2, user3):
    request = app.get(BASE_PATH + str(user1.id))
    assert request.status_code == 200
    assert request.json()['first_name'] == user1.first_name


def test_get_not_found(app: TestClient):
    request = app.get(BASE_PATH + '10000000000')
    assert request.status_code == 404


def test_list(app: TestClient, user1, user2, user3):
    request = app.get(BASE_PATH)
    assert request.status_code == 200
    assert len(request.json()) == 3


def test_list_search(app: TestClient, user1, user2, user3):
    request = app.get(BASE_PATH, params={'first_name': user1.first_name[0:-2]})
    assert request.status_code == 200
    assert len(request.json()) == 1
    assert request.json()[0]['first_name'] == user1.first_name


def test_list_not_found(app: TestClient):
    request = app.get(BASE_PATH)
    assert request.status_code == 200
    assert len(request.json()) == 0


def test_list_friend_id(app: TestClient, user1, user2, user3, friendship):
    request = app.get(BASE_PATH, params={'friends_of': user1.id})
    assert request.status_code == 200
    assert len(request.json()) == 1
    assert request.json()[0]['first_name'] == user2.first_name


def test_list_paginate(app: TestClient, user1, user2, user3):
    request = app.get(BASE_PATH, params={'paginate_by': 1, 'page': 1})
    assert request.status_code == 200
    assert len(request.json()) == 1
    raw_user_1 = request.json()[0]
    request = app.get(BASE_PATH, params={'paginate_by': 1, 'page': 2})
    assert len(request.json()) == 1
    raw_user_2 = request.json()[0]
    assert raw_user_1['id'] != raw_user_2['id']


def test_user_add_hobby(app: TestClient, user1, token1: AccessToken, hobby):
    response = app.put(BASE_PATH + f'hobbies/{hobby.id}',
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 201


def test_user_add_hobby_already_added(app: TestClient, user1,
                                      token1: AccessToken, hobby, user_hobby):
    response = app.put(BASE_PATH + f'hobbies/{hobby.id}',
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 400


def test_user_add_hobby_not_found(app: TestClient, user1, token1: AccessToken,
                                  hobby):
    response = app.put(BASE_PATH + f'hobbies/1000000',
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 400


def test_user_delete_hobby(app: TestClient, user1,
                           token1: AccessToken, hobby, user_hobby):
    response = app.delete(BASE_PATH + f'hobbies/{hobby.id}',
                          headers={'x-auth-token': token1.value})
    assert response.status_code == 204
