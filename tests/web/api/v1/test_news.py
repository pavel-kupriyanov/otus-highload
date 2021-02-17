import pytest
from fastapi.testclient import TestClient

from social_network.db.models import AccessToken, New

BASE_PATH = '/api/v1/news/'


@pytest.fixture(name='clear_news_after')
async def clear_news(cursor):
    yield
    await cursor.execute('DELETE FROM news;')


@pytest.fixture(name='new1')
async def add_new1(factory, user1, clear_news_after):
    return await factory.add_new(user1, 'Hello')


@pytest.fixture(name='new2')
async def add_new2(factory, user2, clear_news_after):
    return await factory.add_new(user2, 'Hi!')


def test_create_new(app: TestClient, user1, token1: AccessToken):
    new = {'text': 'Hello'}
    response = app.post(BASE_PATH, json=new,
                        headers={'x-auth-token': token1.value})
    assert response.status_code == 201
    assert response.json()['payload']['text'] == new['text']


def test_get_news(app: TestClient, token1: AccessToken, new1: New,
                  new2: New):
    response = app.get(BASE_PATH, headers={'x-auth-token': token1.value})
    assert response.status_code == 200
    news = response.json()
    assert len(news) == 1
    assert news[0]['author_id'] == token1.user_id
