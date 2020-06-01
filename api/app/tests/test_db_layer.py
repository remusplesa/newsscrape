from app.db_interface import articles_db
from app.db_interface import keywords_db
import mongomock
import sys
import os
sys.path.insert(0, os.path.abspath('.'))


def test_get_articles_with_one_page():
    articles_collection = mongomock.MongoClient().db.collection
    objects = [{"one": "value", "two": "value"}]
    articles_collection.insert_many(objects)

    res = articles_db.get_articles_mongo(articles_collection, 1, 10)
    assert res["next_page"] == ""
    assert res["previous_page"] == ""
    assert len(res["articles"]) == 1
    mongomock.MongoClient().close()


def test_get_articles_with_multiple_pages():
    articles_collection = mongomock.MongoClient().db.collection
    objects = [{"one": i, "two": i} for i in range(25)]
    articles_collection.insert_many(objects)

    res = articles_db.get_articles_mongo(articles_collection, 1, 10)
    assert res["next_page"] == "/articles/?pageNumber=2&limit=10"
    assert res["previous_page"] == ""
    assert len(res["articles"]) == 10

    res = articles_db.get_articles_mongo(articles_collection, 3, 10)
    assert res["next_page"] == ""
    assert res["previous_page"] == "/articles/?pageNumber=2&limit=10"
    assert len(res["articles"]) == 5

    mongomock.MongoClient().close()


def test_post_articles():
    articles_collection = mongomock.MongoClient().db.collection
    keywords_collection = mongomock.MongoClient().db.collection
    article_to_insert = {
        "source": "https://www.digi24.ro/",
        "publish_date": "25.04.2020 15:15",
        "title": "Demo 2",
        "img_source": "none",
        "tldr": "Test article content",
        "keywords": ["a", "b", "c"],
        "biased": 0.2,
        "clicks": 0,
        "reports": 0,
        "hidden": False,
        "collection_date": 20200505
    }

    res = articles_db.post_articles_mongo(
        articles_collection,
        keywords_collection,
        article_to_insert
    )

    found_article = articles_collection.find_one(
        {"_id": mongomock.ObjectId(res["inserted"])}
    )
    assert article_to_insert == found_article

    articles_in_collection = keywords_collection.count_documents({})
    no_of_inserted_keywords = len(article_to_insert["keywords"])
    assert articles_in_collection == no_of_inserted_keywords

    mongomock.MongoClient().close()


def test_update_article():
    articles_collection = mongomock.MongoClient().db.collection
    article_to_insert = {
        "source": "https://www.digi24.ro/",
        "publish_date": "25.04.2020 15:15",
        "title": "Demo 2",
        "img_source": "none",
        "tldr": "Test article content",
        "keywords": ["a", "b", "c"],
        "biased": 0.2,
        "clicks": 0,
        "reports": 0,
        "hidden": False,
        "collection_date": 20200505
    }

    articles_collection.insert_one(article_to_insert)
    found_article = articles_collection.find_one({})

    res = articles_db.update_articles_mongo(
        articles_collection,
        found_article["_id"],
        "clicks"
    )
    res = articles_db.update_articles_mongo(
        articles_collection,
        found_article["_id"],
        "reports"
    )

    found_article = articles_collection.find_one(
        {"_id": mongomock.ObjectId(res["updated_article"])}
    )

    assert found_article["clicks"] == article_to_insert["clicks"] + 1
    assert found_article["reports"] == article_to_insert["clicks"] + 1

    mongomock.MongoClient().close()


def test_get_keyword():
    keywords_collection = mongomock.MongoClient().db.collection
    keyword_documents = [
        {"word": "a", "date": 20200101, "count": 3},
        {"word": "b", "date": 20200101, "count": 2},
        {"word": "c", "date": 20200101, "count": 1}
    ]
    keywords_collection.insert_many(keyword_documents)

    res = keywords_db.get_keyword_mongo(
        keywords_collection,
        "a",
        20200101,
        20200102
    )

    assert res["word"] == "a"
    assert res["date-range"]["startDate"] == 20200101
    assert res["date-range"]["endDate"] == 20200102
    assert len(res["results"]) == 1


def test_get_top_keywords():
    pass
