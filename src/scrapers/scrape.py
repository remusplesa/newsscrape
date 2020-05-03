import requests
from datetime import datetime
import sys
sys.path.append('..')
from tldr.short_tldr import process_content
from digi import get_from_digi

from bson import json_util
import json



def scrape():
    url = 'http://localhost:8000/articles/'
    articles = get_from_digi()

    for article in articles:
        #print(article)
        response= requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json= vars(article)
            )
        print(response)
scrape()