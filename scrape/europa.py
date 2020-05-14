from article import Article
from api.app.tldr.short_tldr import process_content
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('..')


def get_from_europa():
    website_address = 'https://ec.europa.eu/romania/news_ro'
    # 10 articles per page
    website = requests.get(website_address, 'html/parse')

    soup = BeautifulSoup(
        website.content, features='html.parser', from_encoding="utf-8")
    articles = soup.find_all('div', class_='reps_news_events_wrapper')

    if len(articles) == 0:
        print('No articles found')
        # TODO: try again for 10 times after 1 min.
    else:
        print('Found %d articles in %s ' % (len(articles), website_address))
        page_articles = []

        for article in articles:
            title = str(article.find('a').get_text())
            title = title.replace('&period', '.')\
                .replace('&comma',  ',')\
                .replace('&abreve', 'ă')\
                .replace('&colon',  ';')\
                .replace('&excl',   '!')\
                .replace('&quest',  '?')\
                .replace('&tcedil', 'ț')\
                .replace('&scedil', 'ș')\
                .replace('&semi',   ';')\
                .replace('&vert',   '|')\
                .strip()

            link = 'https://ec.europa.eu/' + \
                str(article.find('a', href=True).attrs['href'])

            content_page = requests.get(link, 'html/parse')
            content = BeautifulSoup(
                content_page.content, features='html.parser')

            article_area = content.find('div', {'class': 'panel-body content'})

            thumb = article_area.find('img', src=True).attrs['src']

            article_content = ''
            for p in article_area.find_all('p'):
                article_content += ' ' + p.get_text().strip()

            tldr, keywords = process_content(article_content, 3)
            if len(tldr) > 255:
                tldr = tldr[:255] + '...'

            publish_date = article_area.find(
                'span', {'class': 'date-display-single'}).get_text().strip()

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

    print('articles from europa: ', len(page_articles))
    return page_articles
