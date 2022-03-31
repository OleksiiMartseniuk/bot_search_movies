import requests

from typing import Optional
from datetime import datetime
from urllib.parse import urljoin

from src.database.db import session
from src.database.models import Movie, Group

from src.config.settings import API_KEY


class InvalidDataRequestError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self):
        return self.message


class InvalidUrlError(Exception):
    pass


class InvalidDataResponse(ValueError):
    pass


class ClientIMDB:
    def __init__(self, api_key: str = API_KEY, domain: str = 'https://imdb-api.com') -> None:
        self.api_key = api_key
        self.domain = domain
        self.session = session
        self.groups = (
            'Top250Movies',
            'Top250TVs',
            'MostPopularMovies',
            'MostPopularTVs'
        )

    def __del__(self):
        self.session.close()

    def _get(self, url_part: str) -> Optional[dict]:
        url = urljoin(self.domain, url_part)
        response = requests.get(url)
        if response.status_code == 200:
            if response.json()['errorMessage']:
                raise InvalidDataRequestError(response.json()['errorMessage'])
            return response.json()
        raise InvalidUrlError

    def collection_data(self) -> None:
        self.clear_data()
        for group_title in self.groups:
            url_part = f'/en/API/{group_title}/{self.api_key}'
            data = self._get(url_part=url_part)
            try:
                # создания групы
                group = Group(title=group_title, created=datetime.now())
                self.session.add(group)
                self.session.commit()
                for item in data['items']:
                    # создания фильма
                    movie = Movie(
                        id_movie=item['id'],
                        rank=int(item['rank']),
                        title=item['title'],
                        full_title=item['fullTitle'],
                        year=item['year'],
                        image=item['image'],
                        crew=item['crew'],
                        imDbRating=item['imDbRating'],
                        imDbRatingCount=int(item['imDbRatingCount']),
                        group=group.id
                    )
                    self.session.add(movie)
                    self.session.commit()
            except InvalidDataResponse as ex:
                raise ex

    def clear_data(self) -> None:
        # очистка таблиць
        self.session.query(Group).delete()
        self.session.query(Movie).delete()
        self.session.commit()
