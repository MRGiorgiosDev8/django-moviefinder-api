from django.urls import path
from .views import home, MovieSearch

urlpatterns = [
    path('', home, name='home'),
    path('api/search/', MovieSearch.as_view(), name='movie-search'),
]