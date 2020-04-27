import requests
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from pymongo import MongoClient
from datetime import datetime


client = MongoClient('mongodb://localhost:27017/')
db = client.newsApp
articles = db.articles

def process_content(text):
    words = word_tokenize(text)
    new_words= [word for word in words if word.isalnum()]
    new_content= [word for word in new_words if word not in stopwords.words('romanian')]
    stemmer = SnowballStemmer("romanian")
    stems = [stemmer.stem(word) for word in new_content]
    fdist = FreqDist(stems)

    sentence = text.lower().split('.')
    org_sentence = text.split('.')

    short = []
    best= []
    for pair in fdist.most_common(5):
        best.append(pair[0])
        
    print('best: ',best)
    for (i,s) in enumerate(sentence):
        words = s.split(' ')
        for word in words:
            if word in best:
                if s not in short and len(short) < 4:
                    short.append(org_sentence[i]+'.')
                    
    tldr=' '.join(short)
    return tldr


def insert_doc(doc: dict):
    articles.insert_one(doc)


def get_from_digi():
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
                .replace('&scedil', 'ș')\
                .strip()
            titles.append(title)

            link = 'https://www.digi24.ro'+str(article.find('a', href=True).attrs['href'])

            content_page = requests.get(link, 'html/parse')
            content = BeautifulSoup(content_page.content, features='html.parser')
            all=''
            for c in content.find_all('p'):
                all+=' '+c.get_text()

            tldr = process_content(all)

            publish_date = content.find('div', {'class': 'author-meta'}).get_text().strip()
            #publish_date = datetime.strptime(publish_date, '%d.%m.%y %H:%M')

            #insert_doc({"source":link, "publish_date": publish_date, "title": title, "img_source": "none", "tldr": tldr, "biased": 0, "clicks": 0})
            print('\n Titlu:' + title,'\n Link:',link,'\n Tldr:',tldr,'\n Publish Date:',publish_date ,'\n')


doc_to_es = {
    "id": "",           #encode the news title+date for id? // later check if id already exists
    "source": "",       #link to redirect the user to
    "publish_date": "", #article publish date
    "title": "",        #article title
    "img_src": "",      #article original thumbnail photo
    "tldr": "",         #processed article content (contains only 5 sentences from the original)
    "biased": "",       #to decide -> calculate some metric of the objectivity of the content
    "clicks": ""        #count no. of article clicks 
}

get_from_digi()
