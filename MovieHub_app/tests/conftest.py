from datetime import date, time

import pytest
from django.contrib.auth.models import User
from django.test import Client
from MovieHub_app.models import Cinema, Movie, Screening, Review, Watchlist

user_counter = 1


@pytest.fixture
def client():
    global user_counter
    username = f'testuser_{user_counter}'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)
    client = Client()
    client.login(username=username, password=password)

    user_counter += 1

    return client


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def cinema():
    return Cinema.objects.create(name='Test Cinema', address='123 Test Street')


@pytest.fixture
def movie():
    return Movie.objects.create(
        title='Test Movie',
        poster_url='http://example.com/poster.jpg',
        release_date=date(2023, 1, 1),
        movie_director='Test Director',
        main_actor='Test Actor'
    )


@pytest.fixture
def screening(cinema, movie):
    return Screening.objects.create(
        movie=movie,
        screening_date=date(2023, 8, 15),
        screening_time=time(18, 30),
        cinema=cinema
    )


@pytest.fixture
def review(user, movie):
    return Review.objects.create(
        user=user,
        movie=movie,
        rating=4,
        comment='Great movie!'
    )


@pytest.fixture
def watchlist(user, movie):
    watchlist = Watchlist.objects.create(user=user)
    watchlist.movies.add(movie)
    return watchlist


@pytest.fixture
def movies():
    return [
        Movie.objects.create(title='Movie 1', release_date='2023-01-01'),
        Movie.objects.create(title='Movie 2', release_date='2023-01-01'),
        Movie.objects.create(title='Movie 3', release_date='2023-01-01'),
    ]


@pytest.fixture
def reviews(user, movies):
    return [
        Review.objects.create(user=user, movie=movies[0], rating=4, comment='Great movie!'),
        Review.objects.create(user=user, movie=movies[1], rating=3, comment='Good movie.'),
        Review.objects.create(user=user, movie=movies[2], rating=5, comment='Excellent movie!')
    ]
