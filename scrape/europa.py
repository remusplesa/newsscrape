import sys
sys.path.append('..')
from scrape import article as art
from scrape.short_tldr import Tldr_content
import requests
import threading
from bs4 import BeautifulSoup


def trim_text(text, length=255):
    if not type(text) == str:
        return TypeError
    if len(text) > length:
        return text[:255] + '...'
    else:
        return text


def get_text(content):
    article_content = ''
    for p in content.find_all('p'):
        article_content += ' ' + p.get_text().strip()
    return article_content


def get_thumbnail(content):
    thumbnail = content.find('img', src=True).attrs['src']
    if len(thumbnail) == 0:
        thumbnail = 'video'
    return thumbnail


def get_articles(article, page_articles):
    title = str(article.find('a').get_text())
    title = title.replace('&period', '.')\
        .replace('&comma', ',')\
        .replace('&abreve', 'ă')\
        .replace('&colon', ';')\
        .replace('&excl', '!')\
        .replace('&quest', '?')\
        .replace('&tcedil', 'ț')\
        .replace('&scedil', 'ș')\
        .replace('&semi', ';')\
        .replace('&vert', '|')\
        .strip()

    link = 'https://ec.europa.eu/' + \
        str(article.find('a', href=True).attrs['href'])

    content_page = requests.get(link, 'html/parse')
    content = BeautifulSoup(
        content_page.content, features='html.parser')
    article_area = content.find('div', {'class': 'panel-body content'})

    thumb = get_thumbnail(article_area)

    article_content = get_text(article_area)

    tl = Tldr_content(article_content, 3)
    tldr, keywords = tl.short()

    tldr = trim_text(tldr)

    publish_date = article_area.find(
        'span', {'class': 'date-display-single'}).get_text().strip()

    if link and title and tldr:
        page_articles.append(
            art.Article(
                link,
                publish_date,
                title,
                thumb,
                tldr,
                keywords,
                0.1
            )
        )


def get_from_europa(website_address='https://ec.europa.eu/romania/news_ro'):
    '''
    Scraper gets articles from ec.europa/roamnia first page.
    Re-runing the scraper multiple times / day saving only the new
    articles provides a steady data stream
    '''
    try:
        website = requests.get(website_address, 'html/parse')
    except requests.exceptions.RequestException:
        return ('Error while connecting to %s' % (website_address))

    soup = BeautifulSoup(
        website.content, features='html.parser', from_encoding="utf-8")
    articles = soup.find_all('div', class_='reps_news_events_wrapper')

    if len(articles) == 0:
        return ValueError('No articles found')
    else:
        print('Found %d articles in %s ' % (len(articles), website_address))

        page_articles = []
        threads = []

        for article in articles:
            t = threading.Thread(
                target=get_articles,
                args=[article, page_articles]
            )
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    print('articles from europa: ', len(page_articles))
    return page_articles


if __name__ == '__main__':
    all = get_from_europa()
    for a in all:
        print(vars(a))
