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
        movies_top = []

        movie_titles = [
            "The Penguin", "The Substance", "Deadpool & Wolverine", "Alien: Romulus",
            "Agatha All Along", "Smile 2", "Arcane", "The Apprentice", "The Batman",
            "Furiosa: A Mad Max Saga", "Joker: Folie à Deux", "The Lord of the Rings: The Rings of Power",
            "The Boys", "The Legend of Vox Machina", "Cyberpunk: Edgerunners", "Loki",
            "Beetlejuice Beetlejuice", "Madame Web", "X-Men '97", "Stranger Things"
        ]

        for title in movie_titles:
            url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
            response = requests.get(url)
            movie_data = response.json()

            if response.status_code == 200 and movie_data.get('Response') != 'False':
                movies_top.append({
                    "Title": movie_data.get('Title'),
                    "Year": movie_data.get('Year'),
                    "Poster": movie_data.get('Poster'),
                    "imdbRating": movie_data.get('imdbRating'),
                    "Genre": movie_data.get('Genre'),
                    "Plot": movie_data.get('Plot'),
                    "imdbID": movie_data.get('imdbID')
                })

        return Response({"movies": movies_top}, status=status.HTTP_200_OK)

class TopActors(APIView):
    def get(self, request):
        api_key = 'e90ced8e264cab6fc8eea78db7a99128'
        actors_top = []

        actor_names = [
            "Cristin Milioti", "Margaret Qualley", "Colin Farrell", "Demi Moore", "Ryan Reynolds",
            "Cailee Spaeny", "Kathryn Hahn", "Aubrey Plaza", "Robert Pattinson", "Anya Taylor-Joy",
            "Zoë Kravitz", "Chris Hemsworth", "Joaquin Phoenix", "Lady Gaga", "Morfydd Clark",
            "Antony Starr", "Erin Moriarty", "Tom Hiddleston", "Sophia Di Martino", "Winona Ryder"
        ]

        for name in actor_names:
            url = f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={name}&language=en-US'
            response = requests.get(url)
            actor_data = response.json()

            if response.status_code == 200 and actor_data.get('results'):
                actor = actor_data['results'][0]
                actors_top.append({
                    "Name": actor.get('name'),
                    "ProfileImage": f"https://image.tmdb.org/t/p/w500{actor.get('profile_path')}" if actor.get('profile_path') else None,
                    "KnownFor": [movie.get('title') or movie.get('name') for movie in actor.get('known_for', [])]
                })

        return Response({"actors": actors_top}, status=status.HTTP_200_OK)