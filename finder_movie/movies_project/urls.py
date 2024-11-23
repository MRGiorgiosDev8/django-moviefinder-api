from django.urls import path
from .views import home, MovieSearch, RandomHighRatedMovies, TopActors

urlpatterns = [
    path('', home, name='home'),
    path('api/search/', MovieSearch.as_view(), name='movie-search'),
    path('api/random-high-rated/', RandomHighRatedMovies.as_view(), name='random-high-rated-movies'),
    path('api/top-actors/', TopActors.as_view(), name='top-actors'),
]