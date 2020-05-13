import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
sys.path.append('..')
from api.app.tldr.short_tldr import process_content
from article import Article

def get_from_mediafax():
    website_address = 'https://www.mediafax.ro/ultimele-stiri/'
    # 50 articles per page
    website = requests.get(website_address, 'html/parse')

    soup = BeautifulSoup(website.content, features='html.parser', from_encoding="utf-8")
    articles_area = soup.find('div', {'class': 'timeline'})
    articles = articles_area.find_all('div', class_='entry')

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
                .replace('&semi', ';')\
                .replace('&vert', '|')\
                .strip()

            link = str(article.find('a', href=True).attrs['href'])


            content_page = requests.get(link, 'html/parse')
            content = BeautifulSoup(content_page.content, features='html.parser')

            article_area = content.find('div', {'class': 'news tabs-container'})
            try:
                thumb = article_area.find('div', {'class': 'ArticleImageContainer'}).find('img').attrs['data-src']
            except:
                thumb = ''

            article_content = ''
            #print(article_area.find('div', {'id': 'article_text_content'}).find('div', {'class': 'just-article-content'}))
            try:
                for p in article_area.find('div', {'id': 'article_text_content'}).find('div', {'class': 'just-article-content'}).find_all('p'):
                    article_content += ' ' + p.get_text().strip()
            except AttributeError:
                continue


            tldr, keywords = process_content(article_content, 3)
            if len(tldr) > 255:
                tldr = tldr[:255] + '...'

            publish_date = article_area.find('dd', {'class': 'date'}).get_text().strip()
            #print('\n Titlu:' + title,'\nThumb: ',thumb,'\n Link:',link,'\n articleContent: ',article_content,'\n Tldr:',tldr,'\n Publish Date:',publish_date ,'\n')
            if link and title and tldr:
                page_articles.append(Article(link, publish_date, title, thumb, tldr, keywords, 0.1))

    print('articles from mediafax: ', len(page_articles))
    return page_articles