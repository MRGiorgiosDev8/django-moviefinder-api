from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def home (request):
    return render(request, 'home.html')

class MovieSearch(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Необходим параметр запроса"}, status=status.HTTP_400_BAD_REQUEST)

        api_key = 'caf8f515'
        url = f'http://www.omdbapi.com/?t={query}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or data.get('Response') == 'False':
            return Response({"error": "Фильм не найден или произошла ошибка API OMDb"}, status=status.HTTP_404_NOT_FOUND)

        movie_data = {
            "Title": data.get('Title'),
            "Year": data.get('Year'),
            "Rated": data.get('Rated'),
            "Released": data.get('Released'),
            "Runtime": data.get('Runtime'),
            "Genre": data.get('Genre'),
            "Director": data.get('Director'),
            "Actors": data.get('Actors'),
            "Plot": data.get('Plot'),
            "Poster": data.get('Poster'),
            "imdbRating": data.get('imdbRating'),
            "imdbID": data.get('imdbID')
        }

        return Response(movie_data, status=status.HTTP_200_OK)