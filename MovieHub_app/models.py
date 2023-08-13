from django.db import models
from django.db.models import Avg


class Cinema(models.Model):
    """
    Model representing a cinema.

    Attributes:
        name (str): The name of the cinema (max length: 64).
        address (str): The address of the cinema (max length: 128).

    Methods:
        __str__(): Returns the string representation of the cinema.
    """
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Model representing a movie.

    Attributes:
        title (str): The title of the movie (max length: 100).
        poster_url (str): The URL of the movie's poster.
        release_date (date): The release date of the movie.
        movie_director (str): The director of the movie (max length: 100).
        main_actor (str): The main actor of the movie (max length: 100).

    Methods:
        __str__(): Returns the string representation of the movie.
        calculate_average_rating(): Calculates the average rating for the movie.
    """
    title = models.CharField(max_length=100)
    poster_url = models.URLField()
    release_date = models.DateField()
    movie_director = models.CharField(max_length=100)
    main_actor = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def calculate_average_rating(self):
        average_rating = \
            (Review.objects.filter(movie=self).aggregate(Avg('rating')))['rating__avg']
        return average_rating or 0


class Screening(models.Model):
    """
    Model representing a movie screening.

    Attributes:
        movie (Movie): The movie being screened.
        screening_date (date): The date of the screening.
        screening_time (time): The time of the screening.
        cinema (Cinema): The cinema where the screening takes place.

    Methods:
        __str__(): Returns the string representation of the screening.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screening_date = models.DateField()
    screening_time = models.TimeField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.cinema.name})"


class Review(models.Model):
    """
    Model representing a movie review.

    Attributes:
        user (User): The user who wrote the review.
        movie (Movie): The movie being reviewed.
        rating (int): The rating given to the movie.
        comment (str): The review comment.

    Methods:
        __str__(): Returns the string representation of the review.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Watchlist(models.Model):
    """
    Model representing a user's movie watchlist.

    Attributes:
        user (User): The user who owns the watchlist.
        movies (ManyToManyField): The movies in the watchlist.

    Methods:
        __str__(): Returns the string representation of the watchlist.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"
