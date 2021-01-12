from fastapi.testclient import TestClient

from social_network.db.models import AccessToken, Friendship

BASE_PATH = '/api/v1/friendships/'


def test_delete(app: TestClient, token1: AccessToken, friendship: Friendship):
    response = app.delete(BASE_PATH + str(friendship.id),
                          headers={'x-auth-token': token1.value})
    assert response.status_code == 204


def test_delete_not_authorized(app: TestClient, friendship):
    response = app.delete(BASE_PATH + str(friendship),
                          json={'user_id': 1},
                          headers={'x-auth-token': 'foobar'})
    assert response.status_code == 401


def test_delete_forbidden(app: TestClient, token3: AccessToken,
                          friendship: Friendship):
    response = app.delete(BASE_PATH + str(friendship.id),
                          headers={'x-auth-token': token3.value})
    assert response.status_code == 403


def test_delete_not_found(app: TestClient, token1: AccessToken, friendship):
    response = app.delete(BASE_PATH + '1000000',
                          headers={'x-auth-token': token1.value})
    assert response.status_code == 404


def test_get(app: TestClient, token1: AccessToken, friendship: Friendship):
    response = app.get(BASE_PATH + str(friendship.id),
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 200


def test_get_not_authorized(app: TestClient, friendship):
    response = app.get(BASE_PATH + str(friendship),
                       json={'user_id': 1},
                       headers={'x-auth-token': 'foobar'})
    assert response.status_code == 401


def test_get_forbidden(app: TestClient, token3: AccessToken,
                       friendship: Friendship):
    response = app.get(BASE_PATH + str(friendship.id),
                       headers={'x-auth-token': token3.value})
    assert response.status_code == 403


def test_get_not_found(app: TestClient, token1: AccessToken, friendship):
    response = app.get(BASE_PATH + '1000000',
                       headers={'x-auth-token': token1.value})
    assert response.status_code == 404
