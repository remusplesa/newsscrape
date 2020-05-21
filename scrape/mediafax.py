import sys
sys.path.append('..')
from scrape import article as art
from api.app.tldr.short_tldr import Tldr_content
import requests
import threading
from bs4 import BeautifulSoup


def trim_text(text):
    if not type(text) == str:
        return TypeError
    if len(text) > 255:
        return text[:255] + '...'
    else:
        return text


def get_text(content):
    article_content = ''
    try:
        for p in content\
                .find('div', {'id': 'article_text_content'})\
                .find('div', {'class': 'just-article-content'})\
                .find_all('p'):
            article_content += ' ' + p.get_text().strip()
    except AttributeError:
        pass
    return article_content


def get_thumbnail(content):
    thumbnail = content\
        .find('div', {'class': 'ArticleImageContainer'})\
        .find('img')\
        .attrs['data-src']

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

    link = str(article.find('a', href=True).attrs['href'])

    content_page = requests.get(link, 'html/parse')
    content = BeautifulSoup(
        content_page.content, features='html.parser')
    article_area = content.find(
        'div', {'class': 'news tabs-container'})

    thumb = get_thumbnail(article_area)

    article_content = get_text(article_area)

    tldr = None
    if article_content:
        tl = Tldr_content(article_content, 3)
        tldr, keywords = tl.short()
        tldr = trim_text(tldr)

    publish_date = article_area.find(
        'dd', {'class': 'date'}).get_text().strip()
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


def get_from_mediafax(
    website_address='https://www.mediafax.ro/ultimele-stiri/'
):
    '''
    Scraper gets articles from digi24/last-news first page.
    Re-runing the scraper multiple times / day saving only the new
    articles provides a steady data stream
    '''
    try:
        website = requests.get(website_address, 'html/parse')
    except requests.exceptions.RequestException:
        return ('Error while connecting to %s' % (website_address))

    soup = BeautifulSoup(
        website.content, features='html.parser', from_encoding="utf-8")
    articles_area = soup.find('div', {'class': 'timeline'})
    articles = articles_area.find_all('div', class_='entry')

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

    print('articles from mediafax: ', len(page_articles))
    return page_articles


if __name__ == '__main__':
    all = get_from_mediafax()
    for a in all:
        print(vars(a))
