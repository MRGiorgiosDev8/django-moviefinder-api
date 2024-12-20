from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая AbstractUser.

    Атрибуты:
        email (EmailField): Уникальный email пользователя.
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """
    Модель профиля пользователя.

    Атрибуты:
        user (OneToOneField): Связь с моделью CustomUser.
        avatar (ImageField): Аватар пользователя.
        birth_date (DateField): Дата рождения пользователя.
        location (CharField): Местоположение пользователя.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"Profile {self.user.username}"


class FavoriteMovie(models.Model):
    """
    Модель избранного фильма.

    Атрибуты:
        user (ForeignKey): Связь с моделью CustomUser.
        title (CharField): Название фильма.
        imdb_id (CharField): Уникальный идентификатор IMDb.
        poster (URLField): URL постера фильма.
        year (CharField): Год выпуска фильма.
        imdb_rating (CharField): Рейтинг IMDb.
        genre (TextField): Жанр фильма.
        plot (TextField): Сюжет фильма.
        actors (TextField): Актеры фильма.
        movie_url (URLField): URL страницы фильма на IMDb.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=50, unique=True)
    poster = models.URLField()
    year = models.CharField(max_length=10)
    imdb_rating = models.CharField(max_length=10, null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    actors = models.TextField(null=True, blank=True)
    movie_url = models.URLField(max_length=500, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.title