from .celery import app
from src.services.imdb_api import ClientIMDB


@app.task
def request_api_imdb():
    """Задача на сбор данных с api IMDB"""
    client = ClientIMDB()
    client.collection_data()


