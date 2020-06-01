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
    # TODO: no previous page in response for first page
    # TODO: no next page in response for last page
    # TODO: length of response == limit
    pass


def test_put_articles():
    # TODO: check if click increment works
    # TODO: check if report increment works
    # TODO: check if article is hidden after x reports
    # TODO: check error handling
    pass


def test_post_articles():
    # TODO: validate the body structure
    # TODO: error handling
    pass


def test_post_tldr():
    # TODO: validate request body
    # TODO: validate response body
    # TODO: validate response body.text == req.sentences
    pass
