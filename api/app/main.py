from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from pydantic import BaseModel, Field, validator
from datetime import datetime
import sys

sys.path.append("..")
from app.routers import articles, tldr, keywords


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


@app.get("/")
def read_root():
    """
    ## Get about api and helpers
    """
    return {
        "hello there": "this is the news API",
        "purpose": "get the latest news articles in Ro. or study statistics about their content",
    }


app.include_router(articles.router)
app.include_router(tldr.router)
app.include_router(keywords.router)
