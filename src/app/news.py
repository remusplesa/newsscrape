from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from pydantic import BaseModel, Field, validator
from datetime import datetime
import sys
sys.path.append('..')
from tldr.short_tldr import process_content


app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('mongodb://localhost:27017/')
db = client.newsApp
articles = db.articles

class Article(BaseModel):
    source: str = Field(..., description='Article source')
    publish_date: str
    title: str = Field(...)
    img_source: str = Field(None, description='Image source')
    tldr: str = Field(..., description='Article body')
    bias: float = Field(None, gt=0, le=1, description='Bias of the news article')
    clicks: int
    reports: int
    hidden: bool
    collection_date: str


    """
    @validator('source')
    def source_is_ok(cls, v):
        for source in ['digi24', 'realitatea', 'protv', 'mediafax']:
            if source not in v:
                return ValueError('Source not accepted')
        return v
        
    @validator(publish_date)
    def date_is_ok(cls, v):
        datetime.strptime(v, '%d.%m%y %H:%M') + strftime
    """


class Tldr(BaseModel):
    sentences: int = Field(..., gt=0, description='Number of sentences to be returned')
    text: str = Field(..., max_length=1000, description='Original text limited to ~2 pages (1000 words)')


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


@app.post('/articles/')
def post_article(article: Article=Body(...)):
    """
    Insert a new document in the db after object validation.
    """
    res = articles.insert_one(article.dict())
    return {"inserted": str(res.inserted_id)}


@app.put('/articles/{article_id}')
def uptdate_article(article_id: str):
    """
    # Increment the click count of an article
    # TODO: Increment the report count
    """
    res = articles.update_one({"_id": ObjectId(article_id)}, {"$inc": {"clicks": 1}})
    return {'updated_article' : res.raw_result}


@app.post('/tldr')
def to_tldr(text: Tldr=Body(...)):
    """
    # TODO: Return a Tldr for any posted(?) text
    """
    out = process_content(text.text, text.sentences)
    return {"tldr": out}
