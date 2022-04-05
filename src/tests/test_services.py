from datetime import datetime
from unittest import TestCase
from src.database.db import create
from src.services.utils import MovieServices
from src.services import imdb_api
from src.database.db import session
from src.database.models import Group, Movie
from src.config.settings import TEST


class MovieServicesTestCase(TestCase):
    def setUp(self) -> None:
        # Значения переменой TEST = True
        # src.config.settings TEST = True

        if not TEST:
            raise ValueError('TEST != True')
        create()
        self.session = session
        for g in range(4):
            group = Group(title=f'group_title_{g}', created=datetime.now())
            self.session.add(group)
            self.session.commit()
            for m in range(6):
                movie = Movie(
                    id_movie=f'id_{m}',
                    rank=m,
                    title=f'title_{m}',
                    full_title=f'fullTitle_{m}',
                    year=f'year_{m}',
                    image=f'image_{m}',
                    crew=f'crew_{m}',
                    imDbRating=f'imDbRating_{m}',
                    imDbRatingCount=m,
                    group=group.id
                )
                self.session.add(movie)
                self.session.commit()

    def test_movie_id(self):
        movie = MovieServices.movie_id(5)
        self.assertEqual(movie.id, 5)
        self.assertEqual(movie.id_movie, 'id_4')
        self.assertEqual(movie.rank, 4)
        self.assertEqual(movie.title, 'title_4')
        self.assertEqual(movie.full_title, 'fullTitle_4')
        self.assertEqual(movie.year, 'year_4')
        self.assertEqual(movie.image, 'image_4')
        self.assertEqual(movie.crew, 'crew_4')
        self.assertEqual(movie.imDbRating, 'imDbRating_4')
        self.assertEqual(movie.imDbRatingCount, 4)

    def test_movie_all(self):
        movie_all = MovieServices('group_title_0').movie_all()
        self.assertEqual(len(movie_all), 6)

    def test_movie_top(self):
        movie_all = MovieServices('group_title_1').movie_top(5)
        self.assertEqual(len(movie_all), 5)

    def test_movie_rang(self):
        movie_rang = MovieServices('group_title_2').movie_rang()
        self.assertIsInstance(movie_rang, Movie)


class ClientIMDBTestCase(TestCase):
    def setUp(self) -> None:
        # Значения переменой TEST = True
        # src.config.settings TEST = True
        if not TEST:
            raise ValueError('TEST != True')
        create()
        self.session = session

    def test_imdb_api(self):
        with self.session as s:
            self.assertEqual(s.query(Movie).count(), 0)
            self.assertEqual(s.query(Group).count(), 0)
        client = imdb_api.ClientIMDB()
        client.collection_data()
        with self.session as s:
            self.assertEqual(s.query(Movie).count(), 700)
            self.assertEqual(s.query(Group).count(), 4)

    def test_invalid_data_request_error(self):
        client = imdb_api.ClientIMDB(api_key='Test')
        with self.assertRaises(imdb_api.InvalidDataRequestError) as context:
            client.collection_data()
        self.assertTrue('Invalid API Key', context.exception)

    def test_invalid_url_error(self):
        with self.session as s:
            self.assertEqual(s.query(Movie).count(), 0)
            self.assertEqual(s.query(Group).count(), 0)
        client = imdb_api.ClientIMDB()
        with self.assertRaises(Exception) as context:
            client._get('/qwe')
        with self.session as s:
            self.assertEqual(s.query(Movie).count(), 0)
            self.assertEqual(s.query(Group).count(), 0)
