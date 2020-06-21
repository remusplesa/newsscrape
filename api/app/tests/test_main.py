from app.main import app
from starlette.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath('.'))


client = TestClient(app)


def test_root():
    response = client.get('/')
    print(response)
    assert response.status_code == 200
    ok_keys = {
        "hello there": "this is the news API",
        "purpose": "get the latest news articles in Ro. or\
                    study statistics about their content",
    }
    res_keys = dict(response.json())
    assert res_keys == ok_keys


def test_get_articles():
    # TODO: check error handling
    pass


def test_put_articles():
    # TODO: check error handling
    pass


def test_post_articles():
    # TODO: error handling
    pass


def test_post_tldr():
    # TODO: check error handling
    pass
