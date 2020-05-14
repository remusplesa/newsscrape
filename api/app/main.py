from app.routers import articles, tldr, keywords
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("..")


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
        "purpose": "get the latest news articles in Ro. or\
                    study statistics about their content",
    }


app.include_router(articles.router)
app.include_router(tldr.router)
app.include_router(keywords.router)
