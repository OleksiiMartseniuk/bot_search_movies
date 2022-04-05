from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.settings import DATABASE_URI, DATABASE_URI_TEST, TEST


Base = declarative_base()
engine = create_engine(DATABASE_URI_TEST if TEST else DATABASE_URI)

session = Session(engine)


def create():
    Base.metadata.create_all(engine)
