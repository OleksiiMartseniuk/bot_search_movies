import os

from src.database.db import create
from src.database.models import Movie, Group
from src.services.imdb_api import ClientIMDB
from src.config.settings import BASE_DIR


if __name__ == '__main__':
    if not os.path.exists(f'{BASE_DIR}/db.sqlite3'):
        if os.getenv('API_KEY'):
            create()
            client = ClientIMDB()
            client.collection_data()
            print('Create DB')
        else:
            print('Not set ("API_KEY") IMDB')
    else:
        print('DB Exists')


