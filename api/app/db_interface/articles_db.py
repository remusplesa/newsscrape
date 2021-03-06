import pymongo
from datetime import datetime
from bson.objectid import ObjectId


def get_articles_mongo(
    articles_collection: pymongo.collection,
    pageNumber: int = 1,
    limit: int = 10
):
    start_index = ((pageNumber - 1) * limit) if pageNumber > 0 else 0
    end_index = pageNumber * limit

    next_url = (
        "/articles/?pageNumber=" + str(pageNumber + 1) + "&limit=" + str(limit)
        if end_index < articles_collection.count_documents({})
        else ""
    )
    prev_url = (
        "/articles/?pageNumber=" + str(pageNumber - 1) + "&limit=" + str(limit)
        if start_index > 0
        else ""
    )

    output = [
        article
        for article in articles_collection.find()
        .sort("_id", pymongo.DESCENDING)
        .skip(start_index)
        .limit(limit)
    ]

    for art in output:
        art["_id"] = str(art["_id"])

    return {
        "next_page": next_url,
        "previous_page": prev_url,
        "articles": output
    }


def get_top_articles_mongo(
    articles_collection: pymongo.collection,
    limit: int,
    date: int
):
    query = {"collection_date": date}

    output = [
        article
        for article in articles_collection.find(query, {"_id": 0})
        .sort("clicks", pymongo.DESCENDING)
        .limit(limit)
    ]

    return {
        "limit": limit,
        "date": date,
        "results": output,
    }


def post_articles_mongo(
    articles_collection: pymongo.collection,
    keywords_collection: pymongo.collection,
    article
):
    exists = True if articles_collection.find_one({
        "source": article["source"]
    }) is not None else False
    print(exists, "exists?")
    if exists is False:
        keywords_to_insert = article['keywords']
        for word in keywords_to_insert:
            keywords_collection.update_one(
                {
                    "$and": [
                        {"word": word},
                        {"date": int(datetime.now().strftime("%Y%m%d"))},
                    ]
                },
                {"$inc": {"count": 1}},
                upsert=True,
            )

        res = articles_collection.insert_one(article)
        return {
            "inserted": str(res.inserted_id),
            "inserted_keywords": keywords_to_insert
        }
    else:
        return {
            "already exists": article["source"]
        }


def update_articles_mongo(articles_collection, article_id, to_update):
    if to_update not in ["clicks", "reports"]:
        # TODO return error code
        return {"error": to_update + " is not updatable"}

    articles_collection.update_one(
        {"_id": ObjectId(article_id)},
        {"$inc": {to_update: 1}}
    )

    return {
        "updated_article": article_id,
        "incremented": to_update
    }
