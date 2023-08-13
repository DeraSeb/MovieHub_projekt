from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, RedirectView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, UserCreateForm, ReviewForm
from .models import Movie, Review, Cinema, Screening, Watchlist


class UserCreateView(FormView):
    """
    Handles user registration through a form submission.

    Attributes:
        form_class (class): The form class for user registration.
        template_name (str): The template to render the registration form.
        success_url (str): The URL to redirect to on successful registration.

    Methods:
        form_valid(form): Handles form submission when valid.
    """
    form_class = UserCreateForm
    template_name = 'registerform.html'
    success_url = '/login'

    def form_valid(self, form):
        data = form.cleaned_data
        data.pop('password_confirmation')
        User.objects.create_user(**data)
        return super().form_valid(form)


class LoginView(View):
    """
    Handles user login and authentication.

    Methods:
        get(request): Handles GET request for rendering login form.
        post(request): Handles POST request for user authentication.
    """

    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'loginform.html', context=ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/main')
            else:
                message = 'Invalid login credentials'
                ctx = {'form': form, 'message': message}
                return render(request, 'loginform.html', context=ctx)


class DashboardView(LoginRequiredMixin, View):
    """
    Displays a dashboard with user-related content.

    Attributes:
        template_name (str): The template to render the dashboard.

    Methods:
        get(request): Handles GET request for rendering the dashboard.
    """
    template_name = 'dashboard.html'

    def get(self, request):
        latest_reviews = Review.objects.order_by('id')[::-1][:3]
        movies = Movie.objects.all()
        movies_ranking = []
        for movie in movies:
            avg_rating = movie.calculate_average_rating()
            movies_ranking.append({'movie': movie, 'avg_rating': avg_rating})
        sorted_ranking = sorted(movies_ranking, key=lambda x: x['avg_rating'], reverse=True)
        ctx = {'reviews': latest_reviews,
               'movies': movies,
               'sorted_ranking': sorted_ranking}
        return render(request, self.template_name, context=ctx)


class CinemaView(View):
    """
    Handles rendering information about a specific movie in different cinemas.

    Methods:
        get(request, movie_id): Handles GET request for rendering cinema details.
    """

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        cinemas = Cinema.objects.all()
        ctx = {'movie': movie,
               'cinemas': cinemas}
        return render(request, 'cinema.html', context=ctx)


class MovieView(View):
    """
    Handles rendering information about a specific movie in a specific cinema.

    Methods:
        get(request, movie_id, cinema_id): Handles GET request for rendering movie details.
    """

    def get(self, request, movie_id, cinema_id):
        movie = Movie.objects.get(pk=movie_id)
        cinema = Cinema.objects.get(pk=cinema_id)
        screenings = Screening.objects.filter(movie=movie, cinema=cinema)
        ctx = {'movie': movie,
               'cinema': cinema,
               'screenings': screenings}

        return render(request, 'movie.html', context=ctx)


class LandingPageView(View):
    """
    Handles rendering the landing page with movie rankings and latest movies.

    Methods:
        get(request): Handles GET request for rendering the landing page.
    """

    def get(self, request):
        movie = Movie.objects.all()
        movies_ranking = []
        latest_movies = Movie.objects.order_by('id')[::-1][:3]
        for movie in movie:
            avg_rating = movie.calculate_average_rating()
            movies_ranking.append({'movie': movie, 'avg_rating': avg_rating})
        sorted_ranking = sorted(movies_ranking, key=lambda x: x['avg_rating'], reverse=True)
        ctx = {'sorted_ranking': sorted_ranking,
               'latest_movies': latest_movies}
        return render(request, 'landingpage.html', context=ctx)


class UserAccountView(LoginRequiredMixin, View):
    """
    Displays user account information including reviews, movie rankings, and watchlist.

    Attributes:
        template_name (str): The template to render the user account page.

    Methods:
        get(request): Handles GET request for rendering user account details.
    """
    template_name = 'account.html'

    def get(self, request):
        user = request.user
        reviews = Review.objects.filter(user=user)

        ranked_movies = []
        for review in reviews:
            avg_rating = review.movie.calculate_average_rating()
            ranked_movies.append({'movie': review.movie, 'avg_rating': avg_rating})
        sorted_ranking = sorted(ranked_movies, key=lambda x: x['avg_rating'], reverse=True)

        watchlist, created = Watchlist.objects.get_or_create(user=user)

        ctx = {
            'reviews': reviews,
            'user': user,
            'sorted_ranking': sorted_ranking,
            'watchlist': watchlist,
        }
        return render(request, self.template_name, context=ctx)


class AddReview(LoginRequiredMixin, View):
    """
    Handles adding new reviews for movies.

    Attributes:
        template_name (str): The template to render the add review page.

    Methods:
        get(request): Handles GET request for rendering the review form.
        post(request): Handles POST request for adding a new review.
    """
    template_name = 'addreview.html'

    def get(self, request):
        form = ReviewForm
        ctx = {'form': form}
        return render(request, self.template_name, context=ctx)

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('main/')
        else:
            form = ReviewForm
            ctx = {'form': form}
            return render(request, self.template_name, context=ctx)


class LogoutView(RedirectView):
    """
    Handles user logout and redirects to the landing page.

    Attributes:
        url (str): The URL to redirect to after logout.

    Methods:
        get(request, *args, **kwargs): Handles GET request for logging out.
    """
    url = reverse_lazy('landingpage')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class AddToWatchlistView(LoginRequiredMixin, View):
    """
    Handles adding a movie to the user's watchlist.

    Methods:
        post(request, movie_id, cinema_id): Handles POST request for adding to watchlist.
    """

    def post(self, request, movie_id, cinema_id):
        movie = Movie.objects.get(id=movie_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist.movies.add(movie)

        return redirect('movie-view', movie_id=movie_id, cinema_id=cinema_id)
