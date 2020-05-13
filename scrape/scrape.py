import requests
from datetime import datetime
import sys
sys.path.append('..')
from api.app.tldr.short_tldr import process_content
from digi import get_from_digi
from europa import get_from_europa
from mediafax import get_from_mediafax

from bson import json_util
import json

def post_article(article):
    url = 'http://localhost:8000/articles/'

    response= requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json= vars(article)
                )
    print(response)

def scrape():

    articles = get_from_digi()
    articles += get_from_europa()
    articles += get_from_mediafax()
    for article in articles:
        print(vars(article))
        post_article(article)

scrape()