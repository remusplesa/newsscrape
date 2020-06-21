FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./api/app/ /app
COPY ./api/app/tldr/ /app/tldr
COPY ./requirements.txt /app

RUN pip install -r requirements.txt
