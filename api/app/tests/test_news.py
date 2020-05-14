from app.main import app
from starlette.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath('.'))


client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    ok_keys = [
        "number_of_articles",
        "number_of_articles_today",
        "number_of_clicks_today"
    ]
    res_keys = list(dict(response.json()).keys())
    assert res_keys == ok_keys


def test_get_articles():
    response = client.get('/articles')
    assert response.status_code == 200
    # TODO: no previous page in response for first page
    # TODO: no next page in response for last page
    # TODO: length of response == limit


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
