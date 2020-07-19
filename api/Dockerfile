FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app/ /app
COPY ./app/tldr/ /app/tldr
COPY ./requirements.txt /app

RUN pip install -r requirements.txt
