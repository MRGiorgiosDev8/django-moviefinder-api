from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    """
    Сериализатор для представления информации о фильме.

    Атрибуты:
        Title (CharField): Название фильма.
        Year (CharField): Год выпуска фильма.
        Poster (URLField): URL постера фильма. Может быть пустым.
        imdbRating (CharField): Рейтинг фильма на IMDb. Может быть пустым.
        Genre (CharField): Жанр фильма. Может быть пустым.
        Plot (CharField): Сюжет фильма. Может быть пустым.
        imdbID (CharField): Уникальный идентификатор фильма на IMDb.
        Actors (CharField): Актеры, снимавшиеся в фильме. Может быть пустым.
    """
    Title = serializers.CharField()
    Year = serializers.CharField()
    Poster = serializers.URLField(allow_blank=True)
    imdbRating = serializers.CharField(allow_blank=True)
    Genre = serializers.CharField(allow_blank=True)
    Plot = serializers.CharField(allow_blank=True)
    imdbID = serializers.CharField()
    Actors = serializers.CharField(allow_blank=True)

class ActorSerializer(serializers.Serializer):
    Name = serializers.CharField()
    ProfileImage = serializers.URLField(allow_blank=True)
    Summary = serializers.CharField(allow_blank=True)
    WikipediaLink = serializers.URLField()
    IMDbLink = serializers.URLField(allow_blank=True)
