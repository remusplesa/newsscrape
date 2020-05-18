import sys
sys.path.append('..')
from article import Article
from api.app.tldr.short_tldr import Tldr_content
import requests
from bs4 import BeautifulSoup
import threading


def trim_text(text):
    if len(text) > 255:
        return text[:255] + '...'
    else:
        return text


def get_article(article, page_articles):
    title = str(article.select('.article-title')[0].get_text())
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

    link = 'https://www.digi24.ro' + \
        str(article.find('a', href=True).attrs['href'])

    content_page = requests.get(link, 'html/parse')
    content = BeautifulSoup(
        content_page.content, features='html.parser')
    thumb = content.find('figure', {'class': 'article-thumb'})\
        .find('img', src=True)\
        .attrs['src']

    article_content = ''
    for c in content.find_all('p'):
        article_content += ' ' + c.get_text().strip()

    tl = Tldr_content(article_content, 3)
    tldr, keywords = tl.short()

    tldr = trim_text(tldr)

    publish_date = content.find('time').get_text().strip()

    if link and title and tldr:
        page_articles.append(
            Article(
                link,
                publish_date,
                title,
                thumb,
                tldr,
                keywords,
                0.1
            )
        )


def get_from_digi(website_address='https://www.digi24.ro/ultimele-stiri'):
    '''
    Scraper gets articles from digi24/last-news first page.
    Re-runing the scraper multiple times / day saving only the new
    articles provides a steady data stream
    '''
    try:
        website = requests.get(website_address, 'html/parse')
    except requests.exceptions.RequestException as e:
        print('%s while connecting to %s' % (e, website_address))

    soup = BeautifulSoup(
        website.content, features='html.parser', from_encoding="utf-8")

    articles = soup.find_all('article', class_='article brdr')

    if len(articles) == 0:
        return ValueError('No articles found')
    else:
        print('Found %d articles in %s ' % (len(articles), website_address))

        page_articles = []
        threads = []

        for article in articles:
            t = threading.Thread(
                target=get_article,
                args=[article, page_articles]
            )
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    print('articles from digi: ', len(page_articles))
    return page_articles


if __name__ == '__main__':
    all = get_from_digi()
    for a in all:
        print(vars(a))
