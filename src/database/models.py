from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base


class Group(Base):
    """Група фильмов"""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    created = Column(DateTime)
    student = relationship('Movie')

    def __repr__(self):
        return f'group: {self.title}'


class Movie(Base):
    """Фильм"""
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    id_movie = Column(String(20))
    rank = Column(Integer)
    title = Column(String(50))
    full_title = Column(String(100))
    year = Column(String(10))
    image = Column(String(1000))
    crew = Column(String(100))
    imDbRating = Column(String)
    imDbRatingCount = Column(Integer)
    group = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return f'movie: {self.title}'
