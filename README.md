# NewsScrape

## 💻 FastAPI CRUD api that interacts with mongoDB 

## 🕸 Web scrapers for popular Romanian news sites [work in progress...]

## 📖 TLDR module that reduces length of text by extracting the most valuable sentences using NLP techniques

<hr/>

## Available endpoints: 
* GET root
    * Basic info about the service
* GET articles
    * Paginated articles from db
* POST articles
    * Validate and Insert article in db
* PUT articles 
    * Update click count & reports of an article
* POST tldr
    * Text shortening w/ NLP endpoint
* GET keywords
    * Returns analytics about the occurence of a word
* GET top_keywords
    * Returns top N words occured in a time interval

### ⚠️ Start the service with uvicorn and navigate to localhost:8000/docs for the full documentation

<hr/>

## Available scrapers: 
* Mediafax.ro
* Digi24.ro
* Europa.eu