"""
URL configuration for MovieHubb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from MovieHub_app import views
from MovieHub_app.views import LoginView, UserCreateView, DashboardView, LandingPageView,\
    UserAccountView, AddReview, MovieView, CinemaView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('', LandingPageView.as_view(), name='landingpage'),
    path('account/', UserAccountView.as_view(), name='account'),
    path('addreview', AddReview.as_view(), name='add-review'),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('cinema/<int:movie_id>/', CinemaView.as_view(), name='cinema-view'),
    path('movie/<int:movie_id>/<int:cinema_id>/', MovieView.as_view(), name='movie-view'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_to_watchlist/<int:movie_id>/<int:cinema_id>', views.AddToWatchlistView.as_view(),
         name='add_to_watchlist'),
]