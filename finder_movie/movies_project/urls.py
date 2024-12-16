from django.urls import path
from .views import home, MovieSearch, RandomHighRatedMovies, TopActors, MostPopularMovies, PopularReleasesActors

app_name = 'movies_project'

urlpatterns = [
    path('', home, name='home'),
    path('api/search/', MovieSearch.as_view(), name='movie-search'),
    path('api/random-high-rated/', RandomHighRatedMovies.as_view(), name='random-high-rated-movies'),
    path('api/top-actors/', TopActors.as_view(), name='top-actors'),
    path('api/most-popular-movies/', MostPopularMovies.as_view(), name='most_popular_movies'),
    path('api/popular-releases-actors/', PopularReleasesActors.as_view(), name='popular_releases_actors'),
]