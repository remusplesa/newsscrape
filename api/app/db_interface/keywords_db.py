import pymongo


def get_keyword_mongo(
    keywords_collection: pymongo.collection,
    word,
    startDate,
    endDate
):
    query = {"$and": [
        {"word": word},
        {"date": {
            "$gte": startDate,
            "$lte": endDate
        }},
    ]}

    output = [article for article in keywords_collection.find(
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


def get_top_keywords(
    keywords_collection: pymongo.collection,
    limit,
    date
):
    query = {"date": date}

    output = [
        article
        for article in keywords_collection.find(query, {"_id": 0, "date": 0})
        .sort("count", pymongo.DESCENDING)
        .limit(limit)
    ]

    return {
        "limit": limit,
        "date": date,
        "results": output,
    }
