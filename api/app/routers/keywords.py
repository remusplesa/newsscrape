from fastapi import APIRouter
from pymongo import MongoClient
import pymongo
from datetime import datetime


router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client.newsApp
keywords = db.keywords


@router.get("/keywords/")
def get_keywords(
    word: str,
    startDate: int,
    endDate: int = int(datetime.now().strftime("%Y%m%d"))
):
    """
    # Get the usage frequency of a keyword in a date range
    """

    query = {"$and": [{"word": word}, {
        "date": {"$gte": startDate, "$lte": endDate}}, ]}

    output = [article for article in keywords.find(
        query, {"_id": 0, "word": 0})]
    total = 0
    for c in output:
        total += c["count"]
    return {
        "word": word,
        "date-range": {"startDate": startDate, "endDate": endDate},
        "results": output,
        "total_count": total,
    }


@router.get("/best_keywords/")
def get_most_used(
    date: int = int(datetime.now().strftime("%Y%m%d")),
    length: int = 10
):
    """
    # Get most used [n] keywords in a day
    """

    query = {"date": date}

    output = [
        article
        for article in keywords.find(query, {"_id": 0, "date": 0})
        .sort("count", pymongo.DESCENDING)
        .limit(length)
    ]

    return {
        "limit": length,
        "date": date,
        "results": output,
    }
