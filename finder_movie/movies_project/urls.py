from django.urls import path
from .views import home, MovieSearch, RandomHighRatedMovies, ActorSearch

urlpatterns = [
    path('', home, name='home'),
    path('api/search/', MovieSearch.as_view(), name='movie-search'),
    path('api/random-high-rated/', RandomHighRatedMovies.as_view(), name='random-high-rated-movies'),
    path('api/actors/', ActorSearch.as_view(), name='actor_search'),
]