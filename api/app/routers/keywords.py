from fastapi import APIRouter
from pymongo import MongoClient
from datetime import datetime
from app.db_interface import keywords_db
from app.credentials import mongo_password


client = MongoClient(
    "mongodb://admin:" + mongo_password + "@mongo:27017/?authSource=newsApp"
)
db = client.newsApp
keywords = db.keywords


router = APIRouter()


@router.get("/keywords/")
def get_keyword_info(
    word: str,
    startDate: int,
    endDate: int = int(datetime.now().strftime("%Y%m%d"))
):
    """
    # Get the usage frequency of a keyword in a date range
    """

    res = keywords_db.get_keyword_mongo(
        keywords,
        word,
        startDate,
        endDate
    )
    return res


@router.get("/top_keywords/")
def get_top_keywords(
    limit: int = 10,
    date: int = None
):
    """
    # Get most used [n] keywords in a day
    """
    if date is None:
        date = int(datetime.now().strftime("%Y%m%d"))

    res = keywords_db.get_top_keywords(
        keywords,
        limit,
        date
    )
    return res
