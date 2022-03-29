import requests
from urllib.parse import urljoin

from settings import API_KEY


class ClientIMDB:
    def __init__(self, api_key: str, domain: str = 'https://imdb-api.com') -> None:
        self.api_key = api_key
        self.domain = domain
    
    def _get(self, url_part: str) -> dict:
        url = urljoin(self.domain, url_part)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {'Error': 'Invalid request'}

    def top_250_movies(self) -> dict:
        # 250 лучших фильмов
        url_part = f'/en/API/Top250Movies/{self.api_key}'
        return self._get(url_part=url_part)

    def top_250_tv_s(self) -> dict:
        # 250 лучших телеcериялов
        url_part = f'/en/API/Top250TVs/{self.api_key}'
        pass

    def most_popular_movies(self) -> dict:
        # Самые популярные фильмы
        url_part = f'/en/API/MostPopularMovies/{self.api_key}'
        pass

    def most_popular_tv_s(self) -> dict:
        # Самые популярные телеcериали
        url_part = f'/en/API/MostPopularTVs/{self.api_key}'
        pass


if __name__ == '__main__':
    client = ClientIMDB(api_key=API_KEY)
    print(client.top_250_movies())