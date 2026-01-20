import requests
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, ActorSerializer

def home(request):
    return render(request, 'home.html')

class MovieSearch(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Необходим параметр запроса"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            api_key = 'caf8f515'
            url = f'http://www.omdbapi.com/?s={query.strip()}&apikey={api_key}'
            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code != 200 or data.get('Response') == 'False':
                return Response({"error": "Фильмы не найдены или ошибка API"}, status=status.HTTP_404_NOT_FOUND)

            movies = []
            for item in data.get('Search', []):
                detail_url = f'http://www.omdbapi.com/?i={item.get("imdbID")}&apikey={api_key}'
                detail_resp = requests.get(detail_url, timeout=5)
                movie_data = detail_resp.json()

                if detail_resp.status_code == 200 and movie_data.get('Response') != 'False':
                    movies.append({
                        "Title": movie_data.get('Title'),
                        "Year": movie_data.get('Year'),
                        "Poster": movie_data.get('Poster'),
                        "imdbRating": movie_data.get('imdbRating'),
                        "Genre": movie_data.get('Genre'),
                        "Plot": movie_data.get('Plot'),
                        "imdbID": movie_data.get('imdbID'),
                        "Actors": movie_data.get('Actors')
                    })

            serializer = MovieSerializer(movies, many=True)
            return Response({"movies": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Ошибка в MovieSearch:", e)
            traceback.print_exc()
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RandomHighRatedMovies(APIView):
    def get(self, request):
        try:
            api_key = 'caf8f515'
            movies_top = []
            titles = [
                "The Penguin", "The Substance", "Deadpool & Wolverine", "Alien: Romulus",
                "Agatha All Along", "Smile 2", "Arcane", "The Apprentice", "The Batman",
                "Furiosa: A Mad Max Saga", "Joker: Folie à Deux", "The Lord of the Rings: The Rings of Power",
                "The Boys", "The Legend of Vox Machina", "Cyberpunk: Edgerunners", "Loki",
                "Beetlejuice Beetlejuice", "Madame Web", "X-Men '97", "Stranger Things"
            ]

            for title in titles:
                url = f'http://www.omdbapi.com/?t={title.strip()}&apikey={api_key}'
                resp = requests.get(url, timeout=5)
                data = resp.json()
                if resp.status_code == 200 and data.get('Response') != 'False':
                    movies_top.append({
                        "Title": data.get('Title'),
                        "Year": data.get('Year'),
                        "Poster": data.get('Poster'),
                        "imdbRating": data.get('imdbRating'),
                        "Genre": data.get('Genre'),
                        "Plot": data.get('Plot'),
                        "imdbID": data.get('imdbID'),
                        "Actors": data.get('Actors')
                    })

            serializer = MovieSerializer(movies_top, many=True)
            return Response({"movies": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Ошибка в RandomHighRatedMovies:", e)
            traceback.print_exc()
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MostPopularMovies(APIView):
    def get(self, request):
        try:
            api_key = 'caf8f515'
            movies_popular = []
            titles = [
                "Kraven the Hunter", "Moana 2", "Nutcrackers", "Peter Pan's Neverland Nightmare",
                "Megalopolis", "The Lord of the Rings: The War of the Rohirrim", "Thunderbolts*", "Heretic",
                "Captain America: Brave New World", "Venom: The Last Dance"
            ]

            for title in titles:
                url = f'http://www.omdbapi.com/?t={title.strip()}&apikey={api_key}'
                resp = requests.get(url, timeout=5)
                data = resp.json()
                if resp.status_code == 200 and data.get('Response') != 'False':
                    movies_popular.append({
                        "Title": data.get('Title'),
                        "Year": data.get('Year'),
                        "Poster": data.get('Poster'),
                        "imdbRating": data.get('imdbRating'),
                        "Genre": data.get('Genre'),
                        "Plot": data.get('Plot'),
                        "imdbID": data.get('imdbID'),
                        "Actors": data.get('Actors')
                    })

            serializer = MovieSerializer(movies_popular, many=True)
            return Response({"movies": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Ошибка в MostPopularMovies:", e)
            traceback.print_exc()
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import time

def fetch_wikipedia_data(actor_name):
    try:
        time.sleep(0.3)
        headers = {
            "User-Agent": "DjangoMovieApp/1.0 (email@george_learning_project.com)"
        }

        wiki_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": actor_name.strip(),
            "prop": "pageimages|extracts",
            "exintro": True,
            "explaintext": True,
            "piprop": "original",
        }
        response = requests.get(wiki_url, params=params, headers=headers, timeout=5)
        if not response.text:
            raise ValueError("Пустой ответ от Wikipedia")
        data = response.json()

        profile_image = None
        summary = None
        link = f"https://en.wikipedia.org/wiki/{actor_name.strip().replace(' ', '_')}"

        if response.status_code == 200:
            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                summary = page.get("extract")
                if page.get("original"):
                    profile_image = page["original"].get("source")

        if not profile_image:
            commons_url = "https://commons.wikimedia.org/w/api.php"
            commons_params = {
                "action": "query",
                "format": "json",
                "prop": "images",
                "titles": f"c:Category:{actor_name.strip()}",
            }
            commons_resp = requests.get(commons_url, params=commons_params, headers=headers, timeout=5)
            if not commons_resp.text:
                raise ValueError("Пустой ответ от Commons")
            commons_data = commons_resp.json()

            pages = commons_data.get('query', {}).get('pages', {})
            for page in pages.values():
                images = page.get('images', [])
                if images:
                    first_image = images[0]['title']
                    image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{first_image.replace('File:', '')}"
                    profile_image = image_url

        return {
            "ProfileImage": profile_image or "",
            "Summary": summary or "",
            "WikipediaLink": link
        }

    except Exception as e:
        print(f" Ошибка Wikipedia для {actor_name}: {e}")
        return {
            "ProfileImage": "",
            "Summary": "",
            "WikipediaLink": f"https://en.wikipedia.org/wiki/{actor_name.strip().replace(' ', '_')}"
        }

class TopActors(APIView):
    def get(self, request):
        try:
            actors_top = []
            links = {
                "Cristin Milioti": "https://www.imdb.com/name/nm2129662/",
                "Colin Farrell": "https://www.imdb.com/name/nm0268199/",
                "Margaret Qualley": "https://www.imdb.com/name/nm4960279/",
                "Demi Moore": "https://www.imdb.com/name/nm0000193/",
                "Ryan Reynolds": "https://www.imdb.com/name/nm0005351/",
                "Cailee Spaeny": "https://www.imdb.com/name/nm8314228/",
                "Kathryn Hahn": "https://www.imdb.com/name/nm1063517/",
                "Aubrey Plaza": "https://www.imdb.com/name/nm2201555/",
                "Robert Pattinson": "https://www.imdb.com/name/nm1500155/",
                "Anya Taylor-Joy": "https://www.imdb.com/name/nm3053338/",
                "Zoë Kravitz": "https://www.imdb.com/name/nm2368789/",
                "Chris Hemsworth": "https://www.imdb.com/name/nm1165110/",
                "Joaquin Phoenix": "https://www.imdb.com/name/nm0001618/",
                "Lady Gaga": "https://www.imdb.com/name/nm3078932/",
                "Ella Purnell": "https://www.imdb.com/name/nm3480246/",
                "Antony Starr": "https://www.imdb.com/name/nm1102278/",
                "Dakota Johnson": "https://www.imdb.com/name/nm0424848/",
                "Tom Hiddleston": "https://www.imdb.com/name/nm1089991/",
                "Sophia Di Martino": "https://www.imdb.com/name/nm1620545/",
                "Winona Ryder": "https://www.imdb.com/name/nm0000213/",
                "Monica Bellucci": "https://www.imdb.com/name/nm0000899/",
                "Willem Dafoe": "https://www.imdb.com/name/nm0000353/",
                "Sebastian Stan": "https://www.imdb.com/name/nm1659221/",
                "Morfydd Clark": "https://www.imdb.com/name/nm6077056/"
            }

            for name, imdb in links.items():
                wiki = fetch_wikipedia_data(name)
                actors_top.append({
                    "Name": name,
                    "ProfileImage": wiki.get("ProfileImage") or "",
                    "Summary": wiki.get("Summary") or "",
                    "WikipediaLink": wiki.get("WikipediaLink") or "",
                    "IMDbLink": imdb or ""
                })

            serializer = ActorSerializer(actors_top, many=True)
            return Response({"actors": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Ошибка в TopActors:", e)
            traceback.print_exc()
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PopularReleasesActors(APIView):
    def get(self, request):
        try:
            actors = []
            links = {
                "Aaron Taylor-Johnson": "https://www.imdb.com/name/nm1093951/",
                "Dwayne Johnson": "https://www.imdb.com/name/nm0425005/",
                "Ben Stiller": "https://www.imdb.com/name/nm0001774/",
                "Linda Cardellini": "https://www.imdb.com/name/nm0004802/",
                "Adam Driver": "https://www.imdb.com/name/nm3485845/",
                "Shia LaBeouf": "https://www.imdb.com/name/nm0479471/",
                "Laurence Fishburne": "https://www.imdb.com/name/nm0000401/",
                "Florence Pugh": "https://www.imdb.com/name/nm6073955/",
                "David Harbour": "https://www.imdb.com/name/nm1092086/",
                "Rachel Weisz": "https://www.imdb.com/name/nm0001838/",
                "Hugh Grant": "https://www.imdb.com/name/nm0000424/",
                "Harrison Ford": "https://www.imdb.com/name/nm0000148/",
                "Liv Tyler": "https://www.imdb.com/name/nm0000239/",
                "Anthony Mackie": "https://www.imdb.com/name/nm1107001/",
                "Tom Hardy": "https://www.imdb.com/name/nm0362766/",
                "Juno Temple": "https://www.imdb.com/name/nm1017334/"
            }

            for name, imdb in links.items():
                wiki = fetch_wikipedia_data(name)
                actors.append({
                    "Name": name,
                    "ProfileImage": wiki.get("ProfileImage") or "",
                    "Summary": wiki.get("Summary") or "",
                    "WikipediaLink": wiki.get("WikipediaLink") or "",
                    "IMDbLink": imdb or ""
                })

            return Response({"actors": actors}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Ошибка в PopularReleasesActors:", e)
            traceback.print_exc()
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)