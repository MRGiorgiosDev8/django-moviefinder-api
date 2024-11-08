from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return render(request, 'home.html')


class MovieSearch(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Необходим параметр запроса"}, status=status.HTTP_400_BAD_REQUEST)

        api_key = 'caf8f515'
        url = f'http://www.omdbapi.com/?s={query}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or data.get('Response') == 'False':
            return Response({"error": "Фильмы не найдены или произошла ошибка API OMDb"}, status=status.HTTP_404_NOT_FOUND)

        movies = []
        for item in data.get('Search', []):
            movies.append({
                "Title": item.get('Title'),
                "Year": item.get('Year'),
                "Poster": item.get('Poster'),
                "imdbID": item.get('imdbID')
            })

        return Response({"movies": movies}, status=status.HTTP_200_OK)