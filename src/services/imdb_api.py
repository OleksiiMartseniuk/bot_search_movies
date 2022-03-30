import requests

from datetime import datetime
from urllib.parse import urljoin

from src.database.db import session
from src.database.models import Movie, Groups

from src.config.settings import API_KEY


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

    def _get(self, url_part: str) -> dict:
        url = urljoin(self.domain, url_part)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def data_collection(self) -> None:
        for group_title in self.groups:
            url_part = f'/en/API/{group_title}/{self.api_key}'
            data = self._get(url_part=url_part)
            try:
                # создания групы
                group = Groups(title=group_title, created=datetime.now())
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
                        imDbRatingCount=int(item['imDbRatingCount'])
                    )
                    self.session.add(movie)
                    # добавления фильма в групу
                    group.movies.append(movie)
                    self.session.add(group)
                    self.session.commit()
            except:
                raise Exception
