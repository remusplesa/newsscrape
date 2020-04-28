from starlette.testclient import TestClient
import pytest
import sys
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from ..app.news import app


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

    