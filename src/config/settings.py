import os
from pathlib import Path

API_KEY = os.getenv('API_KEY')
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_URI = f'sqlite:///{BASE_DIR}/db.sqlite3'
