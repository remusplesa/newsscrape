import sys
sys.path.append('..')
from mediafax import get_from_mediafax
from europa import get_from_europa
from digi import get_from_digi
import requests
import threading
import time


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
    threads = []
    for article in articles:
        t = threading.Thread(target=post_article, args=[article])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    while True:
        scrape()
        time.sleep(300)
