import random

from src.database.db import session
from src.database.models import Group, Movie

from sqlalchemy import desc


class MovieServices:
    def __init__(self, group_title: str):
        self.group_title = group_title
        self.session = session

    @staticmethod
    def movie_id(id: int) -> Movie:
        """ Вывод фильма по id"""
        with session as s:
            result = s.query(Movie).filter(Movie.id == id).first()
        return result

    def movie_all(self) -> list:
        """ Вывод всех фильмов """
        with self.session as s:
            result = s.query(Movie).join(Group).filter(Group.title == self.group_title).all()
        return result

    def movie_top(self, values) -> list:
        """ Топ фильмов [1 : values]"""
        with self.session as s:
            result = s.query(Movie).join(Group).filter(Group.title == self.group_title)[:values]
        return result

    def movie_rang(self) -> Movie:
        """ Рандомный фильм """
        with self.session as s:
            first = s.query(Movie).join(Group).filter(Group.title == self.group_title).order_by(Movie.id).first()
            last = s.query(Movie).join(Group).filter(Group.title == self.group_title).order_by(desc(Movie.id)).first()
            id = random.randint(first.id, last.id)
            result = s.query(Movie).get(id)
        return result

