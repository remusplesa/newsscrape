FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./src/app/ /app
COPY ./src/tldr/ /app/tldr
COPY ./requirements.txt /app

RUN pip install -r requirements.txt
