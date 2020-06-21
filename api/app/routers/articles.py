from fastapi import APIRouter, Body
from pymongo import MongoClient
from pydantic import BaseModel, Field
from app.db_interface import articles_db
from app.credentials import mongo_password


class Article(BaseModel):
    source: str = Field(..., description="Article source")
    publish_date: str
    title: str = Field(...)
    img_source: str = Field(None, description="Image source")
    tldr: str = Field(..., description="Article body")
    keywords: list
    bias: float = Field(
        None, gt=0, le=1, description="Bias of the news article")
    clicks: int
    reports: int
    hidden: bool
    collection_date: int

    # TODO pydantic validators


client = MongoClient(
    "mongodb://admin:" + mongo_password + "@mongo:27017/?authSource=newsApp")
db = client.newsApp
articles = db.articles
keywords = db.keywords


router = APIRouter()


@router.get("/articles/")
def get_articles_pagination(pageNumber: int = 0, limit: int = 10):
    """
    # Get articles with pagination
    """
    res = articles_db.get_articles_mongo(
        articles,
        pageNumber,
        limit
    )

    return res


@router.post("/articles/")
def post_new_article(article: Article = Body(...)):
    """
    # Insert a new document in the db after object validation.
    * Insert article in the articles collection
    * Insert keyword in the keywords collection
    (each keyword gets a document / day)
    """
    article_to_insert = article.dict()

    res = articles_db.post_articles_mongo(
        articles,
        keywords,
        article_to_insert
    )
    return res


@router.put("/articles/{article_id}")
def increment_article_field(article_id: str, to_update: str):
    """
    ## Increment the click count of an article
    ## Increment the report count and change the state to hidden
    """
    res = articles_db.update_articles_mongo(
        articles,
        article_id,
        to_update
    )
    return res
