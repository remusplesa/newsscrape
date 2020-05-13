from fastapi import APIRouter, Body, HTTPException
from pymongo import MongoClient
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

from pydantic import BaseModel, Field, validator

router = APIRouter()


class Article(BaseModel):
    source: str = Field(..., description="Article source")
    publish_date: str
    title: str = Field(...)
    img_source: str = Field(None, description="Image source")
    tldr: str = Field(..., description="Article body")
    keywords: list
    bias: float = Field(None, gt=0, le=1, description="Bias of the news article")
    clicks: int
    reports: int
    hidden: bool
    collection_date: int

    # TODO pydantic validators


client = MongoClient("mongodb://localhost:27017/")
db = client.newsApp
articles = db.articles
keywords = db.keywords


@router.get("/articles/")
def get_articles(pageNumber: int = 0, limit: int = 10):
    """
    # Get articles with pagination
    """
    start_index = ((pageNumber - 1) * limit) if pageNumber > 0 else 0
    end_index = pageNumber * limit

    next_url = (
        "/articles/?pageNumber=" + str(pageNumber + 1) + "&limit=" + str(limit)
        if end_index < articles.count_documents({})
        else ""
    )
    prev_url = (
        "/articles/?pageNumber=" + str(pageNumber - 1) + "&limit=" + str(limit)
        if start_index > 0
        else ""
    )

    output = [
        article
        for article in articles.find()
        .sort("_id", pymongo.DESCENDING)
        .skip(start_index)
        .limit(limit)
    ]

    for art in output:
        art["_id"] = str(art["_id"])

    return {"next_page": next_url, "previous_page": prev_url, "articles": output}


@router.post("/articles/")
def post_article(article: Article = Body(...)):
    """
    # Insert a new document in the db after object validation.
    * Insert article in the articles collection
    * Insert keyword in the keywords collection (each keyword gets a document / day)
    """
    keywords_to_insert = article.dict()["keywords"]
    for word in keywords_to_insert:
        keywords.update_one(
            {
                "$and": [
                    {"word": word},
                    {"date": int(datetime.now().strftime("%Y%m%d"))},
                ]
            },
            {"$inc": {"count": 1}},
            upsert=True,
        )

    res = articles.insert_one(article.dict())
    return {"inserted": str(res.inserted_id)}


@router.put("/articles/{article_id}")
def uptdate_article(article_id: str, to_update: str):
    """
    ## Increment the click count of an article
    ## Increment the report count and change the state to hidden
    """
    if to_update not in ["clicks", "reports"]:
        # TODO return error code
        return {"error": to_update + " is not a method"}
    res = articles.update_one({"_id": ObjectId(article_id)}, {"$inc": {to_update: 1}})
    return {"updated_article": article_id, "incremented": to_update}
