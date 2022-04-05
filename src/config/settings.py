import os
from pathlib import Path

API_KEY = os.getenv('API_KEY')
BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEST = False

DATABASE_URI = f'sqlite:///{BASE_DIR}/db.sqlite3'
DATABASE_URI_TEST = "sqlite:///:memory:"
