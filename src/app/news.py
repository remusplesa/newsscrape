from fastapi import FastAPI
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps

app = FastAPI()

mock_data  = [
    {
    "id": 123,           #encode the news title+date for id? // later check if id already exists
    "source": "www.digi.ro",       #link to redirect the user to
    "publish_date": "12.03.2020", #article publish date
    "title": "Abc Defghij klmnopqrstuv wxyz",        #article title
    "img_src": "trhrhtrth",      #article original thumbnail photo
    "tldr": "dfbnvdfjkbvkdfjnbdkfbnkdfjdfb gfbdfkjbvndajkbdajfbnkdjfbv fjdkbvnkjdfabnkadbfkdfjbv dfkjbvjbvadkjfbkdfb",         #processed article content (contains only 5 sentences from the original)
    "biased": "0.2",       #to decide -> calculate some metric of the objectivity of the content
    "clicks": 12        #count no. of article clicks 
},
{
    "id": 123,           #encode the news title+date for id? // later check if id already exists
    "source": "www.digi.ro",       #link to redirect the user to
    "publish_date": "12.03.2020", #article publish date
    "title": "Abc Defghij klmnopqrstuv wxyz",        #article title
    "img_src": "trhrhtrth",      #article original thumbnail photo
    "tldr": "dfbnvdfjkbvkdfjnbdkfbnkdfjdfb gfbdfkjbvndajkbdajfbnkdjfbv fjdkbvnkjdfabnkadbfkdfjbv dfkjbvjbvadkjfbkdfb",         #processed article content (contains only 5 sentences from the original)
    "biased": "0.2",       #to decide -> calculate some metric of the objectivity of the content
    "clicks": 2        #count no. of article clicks 
}]

client = MongoClient('mongodb://localhost:27017/')
db = client.newsApp
articles = db.articles


@app.get('/')
def read_root():
    """
    ## Get statistics for the day
    * ### total no. of articles
    * ### daily no. of articles
    * ### daily no. of clicks
    TODO: get just some stats here
    """
    count = 0
    for article in articles.find({}): #TODO: sort by date here
        count += article['clicks'] 

    return {
        "number_of_articles": articles.count_documents({}),
        "number_of_articles_today": 111,
        "number_of_clicks_today": count
    }


@app.get('/articles/')
def get_articles(pageNumber: int = 0, limit: int = 10):
    """
    # TODO: Get articles with pagination
    """
    start_index = ((pageNumber - 1 ) * limit) if pageNumber > 0 else 0
    end_index = pageNumber * limit

    next_url = '/articles/?pageNumber=' + str(pageNumber + 1) + '&limit=' + str(limit) if end_index < articles.count_documents({}) else ''
    prev_url = '/articles/?pageNumber=' + str(pageNumber - 1) + '&limit=' + str(limit) if start_index > 0 else ''

    output = [article for article in articles.find()
        .sort('_id', pymongo.DESCENDING)
        .skip(start_index)
        .limit(limit)]

    for art in output:
        art['_id'] = str(art['_id'])

    return {
        'next_page': next_url,
        'previous_page': prev_url,
        'articles': output
    }


@app.post('/articles/{article_id}')
def post_article(id):
    """
    # TODO: validate object with pydantic !!??
    # TODO: insert the doc in the db
    """
    pass


@app.put('/articles/{article_id}')
def uptdate_article(article_id: int, value: int = None):
    """
    # TODO: Increment the click count of an article
    """
    #articles.update_one
    return {'updated_article' : article_id}


@app.get('/tldr')
def tldr(text: str):
    """
    # TODO: Return a Tldr for any posted(?) text
    """
    pass
