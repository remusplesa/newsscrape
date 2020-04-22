import requests
from bs4 import BeautifulSoup

website_address = 'https://www.digi24.ro/ultimele-stiri'
website = requests.get(website_address, 'html/parse')

soup = BeautifulSoup(website.content, features='html.parser', from_encoding="utf-8")
articles = soup.find_all('article', class_='article brdr')

if len(articles) == 0:
    print('No articles found')
    # TODO: try again for 10 times after 1 min.
else:
    print('Found %d articles in %s ' % (len(articles), website_address))
    titles = []
    for article in articles:
        title = str(article.select('.article-title')[0].get_text())
        title = title.replace('&period', '.')\
            .replace('&comma',  ',')\
            .replace('&abreve', 'ă')\
            .replace('&colon',  ';')\
            .replace('&excl',   '!')\
            .replace('&quest',  '?')\
            .replace('&tcedil', 'ț')\
            .strip()
        titles.append(title)

        link = 'https://www.digi24.ro'+str(article.find('a', href=True).attrs['href'])

        content_page = requests.get(link, 'html/parse')
        content = BeautifulSoup(content_page.content, features='html.parser')
        all=''
        for c in content.find_all('p'):
            all+=' '+c.get_text()
        publish_date = content.find('div', {'class': 'author-meta'}).get_text()


        print('\n Titlu:' + title,'\n Link:',link,'\n Content:',all,'\n Publish Date:',publish_date ,'\n')

    #print(titles)
