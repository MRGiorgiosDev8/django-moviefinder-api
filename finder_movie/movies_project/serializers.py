from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
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
