from mediafax import get_from_mediafax
from europa import get_from_europa
from digi import get_from_digi
import requests
import sys
sys.path.append('..')


def post_article(article):
    url = 'http://localhost:8000/articles/'

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=vars(article)
    )
    print(response)


def scrape():

    articles = get_from_digi()
    articles += get_from_europa()
    articles += get_from_mediafax()
    for article in articles:
        print(vars(article))
        post_article(article)


if __name__ == '__main__':
    scrape()
