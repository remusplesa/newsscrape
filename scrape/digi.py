import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
sys.path.append('..')
from api.app.tldr.short_tldr import process_content
from article import Article

def get_from_digi():
    website_address = 'https://www.digi24.ro/ultimele-stiri'
    # 50 articles per page
    website = requests.get(website_address, 'html/parse')

    soup = BeautifulSoup(website.content, features='html.parser', from_encoding="utf-8")
    articles = soup.find_all('article', class_='article brdr')

    if len(articles) == 0:
        print('No articles found')
        # TODO: try again for 10 times after 1 min.
    else:
        print('Found %d articles in %s ' % (len(articles), website_address))
        page_articles = []

        for article in articles:
            title = str(article.select('.article-title')[0].get_text())
            title = title.replace('&period', '.')\
                .replace('&comma',  ',')\
                .replace('&abreve', 'ă')\
                .replace('&colon',  ';')\
                .replace('&excl',   '!')\
                .replace('&quest',  '?')\
                .replace('&tcedil', 'ț')\
                .replace('&scedil', 'ș')\
                .replace('&semi', ';')\
                .replace('&vert', '|')\
                .strip()

            link = 'https://www.digi24.ro'+str(article.find('a', href=True).attrs['href'])

            content_page = requests.get(link, 'html/parse')
            content = BeautifulSoup(content_page.content, features='html.parser')


            thumb = content.find('figure', {'class': 'article-thumb'}).find('img', src=True).attrs['src']

            article_content = ''
            for c in content.find_all('p'):
                article_content += ' ' + c.get_text().strip()

            tldr, keywords = process_content(article_content, 3)
            if len(tldr) > 255:
                tldr = tldr[:255] + '...'

            publish_date = content.find('time').get_text().strip()

            if link and title and tldr:
                page_articles.append(Article(link, publish_date, title, thumb, tldr, keywords, 0.1))
                
    print('articles from digi: ', len(page_articles))
    return page_articles
