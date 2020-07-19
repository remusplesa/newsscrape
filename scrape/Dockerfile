FROM python:3

COPY . /scrape

WORKDIR scrape 
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

CMD [ "python", "main.py" ]

