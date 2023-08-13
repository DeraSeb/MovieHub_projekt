import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.template.loader import render_to_string

from MovieHub_app.views import *


@pytest.mark.django_db
def test_user_registration(client):
    client = client
    response = client.get(reverse('user-create'))
    assert response.status_code == 200

    data = {
        'username': 'newuser',
        'password': 'newpassword',
        'password_confirmation': 'newpassword',
        'email': 'newuser@example.com'
    }
    response = client.post(reverse('user-create'), data)
    assert response.status_code == 302
    assert response.url == '/login'

    assert User.objects.filter(username='newuser').exists()

    login_response = client.login(username='newuser', password='newpassword')
    assert login_response is True


@pytest.mark.django_db
def test_user_login(client, user):
    response = client.get(reverse('login'))
    assert response.status_code == 200

    data = {
        'login': 'testuser',
        'password': 'testpassword'
    }
    response = client.post(reverse('login'), data)
    assert response.status_code == 302
    assert response.url == '/main'

    assert '_auth_user_id' in client.session
    assert int(client.session['_auth_user_id']) == user.id


@pytest.mark.django_db
def test_movie_view(client, movie, cinema, screening):
    client = client

    response = client.get(reverse('movie-view', args=[movie.id, cinema.id]))
    assert response.status_code == 200

    assert 'movie' in response.context
    assert 'cinema' in response.context
    assert 'screenings' in response.context

    assert response.context['movie'] == movie
    assert response.context['cinema'] == cinema
    assert list(response.context['screenings']) == [screening]


@pytest.mark.django_db
def test_landing_page_view(client, movies, reviews):
    client = client

    response = client.get(reverse('landingpage'))
    assert response.status_code == 200

    assert 'sorted_ranking' in response.context
    assert 'latest_movies' in response.context

    sorted_ranking = response.context['sorted_ranking']
    assert len(sorted_ranking) == len(movies)

    latest_movies = response.context['latest_movies']
    assert len(latest_movies) == 3

    for ranking_item in sorted_ranking:
        assert ranking_item['movie'] in movies


@pytest.mark.django_db
def test_landing_page_view_empty(client):
    client = client

    response = client.get(reverse('landingpage'))
    assert response.status_code == 200

    assert 'sorted_ranking' in response.context
    assert 'latest_movies' in response.context

    assert len(response.context['sorted_ranking']) == 0
    assert len(response.context['latest_movies']) == 0
