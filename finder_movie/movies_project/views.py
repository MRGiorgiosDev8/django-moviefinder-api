from django.shortcuts import render
import requests
import random
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
            movie_details_url = f'http://www.omdbapi.com/?i={item.get("imdbID")}&apikey={api_key}'
            movie_response = requests.get(movie_details_url)
            movie_data = movie_response.json()

            if movie_response.status_code == 200 and movie_data.get('Response') != 'False':
                movies.append({
                    "Title": movie_data.get('Title'),
                    "Year": movie_data.get('Year'),
                    "Poster": movie_data.get('Poster'),
                    "imdbRating": movie_data.get('imdbRating'),
                    "Genre": movie_data.get('Genre'),
                    "Plot": movie_data.get('Plot'),
                    "imdbID": movie_data.get('imdbID')
                })

        return Response({"movies": movies}, status=status.HTTP_200_OK)


class RandomHighRatedMovies(APIView):
    def get(self, request):
        api_key = 'caf8f515'
        high_rated_movies = []
        rating_threshold = 7.0

        random_keywords = ["action", "adventure", "comedy", "drama", "horror", "sci-fi", "fantasy", "romance"]
        random.shuffle(random_keywords)

        for keyword in random_keywords[:5]:
            url = f'http://www.omdbapi.com/?s={keyword}&apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data.get('Response') != 'False':
                for item in data.get('Search', []):
                    movie_details_url = f'http://www.omdbapi.com/?i={item.get("imdbID")}&apikey={api_key}'
                    movie_response = requests.get(movie_details_url)
                    movie_data = movie_response.json()

                    if movie_data.get('imdbRating') and float(movie_data.get('imdbRating')) >= rating_threshold:
                        high_rated_movies.append({
                            "Title": movie_data.get('Title'),
                            "Year": movie_data.get('Year'),
                            "Poster": movie_data.get('Poster'),
                            "imdbRating": movie_data.get('imdbRating'),
                            "imdbID": movie_data.get('imdbID')
                        })

        return Response({"movies": high_rated_movies}, status=status.HTTP_200_OK)