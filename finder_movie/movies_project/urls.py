from django.urls import path
from .views import MovieSearch, home

urlpatterns = [
    path('', home, name='home'),
    path('search/', MovieSearch.as_view(), name='movie-search'),
]