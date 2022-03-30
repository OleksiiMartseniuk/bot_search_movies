from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.settings import DATABASE_URI


Base = declarative_base()
engine = create_engine(DATABASE_URI)

session = Session(engine)


def create():
    Base.metadata.create_all(engine)
