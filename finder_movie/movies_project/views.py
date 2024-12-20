from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, ActorSerializer

def home(request):
    """
    Обрабатывает запрос на главную страницу и возвращает HTML-шаблон 'home.html'.

    Args:
        request: Объект запроса, содержащий данные о запросе от клиента.

    Returns:
        HttpResponse: Ответ с отрендеренным HTML-шаблоном 'home.html'.
    """
    return render(request, 'home.html')

class MovieSearch(APIView):
    """
    Класс MovieSearch, наследующий APIView, предоставляет метод для поиска фильмов по запросу.

    Методы:
        get(self, request):
            Обрабатывает GET-запрос для поиска фильмов по заданному параметру запроса 'query'.
            Если параметр запроса отсутствует, возвращает ошибку 400.
            Выполняет запрос к API OMDb для поиска фильмов по названию.
            Если фильмы не найдены или произошла ошибка API, возвращает ошибку 404.
            Для каждого найденного фильма выполняет дополнительный запрос для получения подробной информации.
            Возвращает список фильмов в формате JSON с подробной информацией о каждом фильме.
    """
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
                    "imdbID": movie_data.get('imdbID'),
                    "Actors": movie_data.get('Actors')
                })

        serializer = MovieSerializer(movies, many=True)
        return Response({"movies": serializer.data}, status=status.HTTP_200_OK)


class RandomHighRatedMovies(APIView):
    """
    Класс представления фильмов.

    Методы:
    get(self, request):
        Обрабатывает GET-запрос для получения информации о фильмах с использованием OMDB API.
        Возвращает JSON-ответ с данными о фильмах.

    Атрибуты:
    api_key (str): Ключ API для доступа к OMDB API.
    movies_top (list): Список для хранения информации о фильмах.
    movie_titles (list): Список названий фильмов для запроса к OMDB API.
    """
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
                    "imdbID": movie_data.get('imdbID'),
                    "Actors": movie_data.get('Actors')
                })

        serializer = MovieSerializer(movies_top, many=True)
        return Response({"movies": serializer.data}, status=status.HTTP_200_OK)

class MostPopularMovies(APIView):
    """
        Аналогичный класс представления фильмов, но для популярных фильмов.
    """
    def get(self, request):
        api_key = 'caf8f515'
        most_popular_titles = [
            "Kraven the Hunter", "Moana 2", "Nutcrackers", "Peter Pan's Neverland Nightmare",
            "Megalopolis", "The Lord of the Rings: The War of the Rohirrim", "Thunderbolts*", "Heretic",
            "Captain America: Brave New World",  "Venom: The Last Dance"
        ]

        movies_popular = []

        for title in most_popular_titles:
            url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
            response = requests.get(url)
            movie_data = response.json()

            if response.status_code == 200 and movie_data.get('Response') != 'False':
                movies_popular.append({
                    "Title": movie_data.get('Title'),
                    "Year": movie_data.get('Year'),
                    "Poster": movie_data.get('Poster'),
                    "imdbRating": movie_data.get('imdbRating'),
                    "Genre": movie_data.get('Genre'),
                    "Plot": movie_data.get('Plot'),
                    "imdbID": movie_data.get('imdbID'),
                    "Actors": movie_data.get('Actors')
                })

        serializer = MovieSerializer(movies_popular, many=True)
        return Response({"movies": serializer.data}, status=status.HTTP_200_OK)


def fetch_wikipedia_data(actor_name):
    """
    Получает данные из Википедии для указанного актера.

    Аргументы:
    actor_name (str): Имя актера, для которого нужно получить данные.

    Возвращает:
    dict: Словарь с ключами "ProfileImage", "Summary" и "WikipediaLink".
        - "ProfileImage" (str или None): URL изображения профиля актера, если доступно.
        - "Summary" (str или None): Краткое описание актера из Википедии.
        - "WikipediaLink" (str): Ссылка на страницу актера в Википедии.
    """
    wiki_url = "https://en.wikipedia.org/w/api.php"
    wiki_params = {
        "action": "query",
        "format": "json",
        "titles": actor_name,
        "prop": "pageimages|extracts",
        "exintro": True,
        "explaintext": True,
        "piprop": "original",
    }
    wiki_response = requests.get(wiki_url, params=wiki_params)
    wiki_data = wiki_response.json()

    profile_image = None
    summary = None
    wikipedia_link = f"https://en.wikipedia.org/wiki/{actor_name.replace(' ', '_')}"

    if wiki_response.status_code == 200:
        pages = wiki_data.get('query', {}).get('pages', {})
        for page_id, page in pages.items():
            if page_id != "-1":
                profile_image = page.get("original", {}).get("source")
                summary = page.get("extract")

    return {
        "ProfileImage": profile_image,
        "Summary": summary,
        "WikipediaLink": wikipedia_link
    }

class TopActors(APIView):
    """
    Представление для получения списка актеров с информацией из IMDb и Wikipedia.

    Методы:
    get(self, request) -- Обрабатывает GET-запрос и возвращает список актеров с их профилями, краткой информацией и ссылками на IMDb и Wikipedia.
    """
    def get(self, request):
        actors_top = []
        actor_imdb_links = {
            "Cristin Milioti": "https://www.imdb.com/name/nm2129662/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_cristin",
            "Colin Farrell": "https://www.imdb.com/name/nm0268199/?ref_=nv_sr_srsg_0_tt_1_nm_7_in_0_q_Colin%2520Farrell",
            "Margaret Qualley": "https://www.imdb.com/name/nm4960279/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_Margaret%2520Qualley",
            "Demi Moore": "https://www.imdb.com/name/nm0000193/?ref_=fn_al_nm_1",
            "Ryan Reynolds": "https://www.imdb.com/name/nm0005351/?ref_=fn_al_nm_1",
            "Cailee Spaeny": "https://www.imdb.com/name/nm8314228/?ref_=fn_al_nm_1",
            "Kathryn Hahn": "https://www.imdb.com/name/nm1063517/?ref_=fn_al_nm_1",
            "Aubrey Plaza": "https://www.imdb.com/name/nm2201555/?ref_=fn_al_nm_1",
            "Robert Pattinson": "https://www.imdb.com/name/nm1500155/?ref_=nv_sr_srsg_0_tt_5_nm_3_in_0_q_Robert%2520Pattinson",
            "Anya Taylor-Joy": "https://www.imdb.com/name/nm3053338/",
            "Zoë Kravitz": "https://www.imdb.com/name/nm2368789/?ref_=fn_al_nm_1",
            "Chris Hemsworth": "https://www.imdb.com/name/nm1165110/?ref_=nv_sr_srsg_0_tt_7_nm_1_in_0_q_Chris%2520Hemsworth",
            "Joaquin Phoenix": "https://www.imdb.com/name/nm0001618/?ref_=nv_sr_srsg_0_tt_4_nm_1_in_0_q_Joaquin%2520Phoenix",
            "Lady Gaga": "https://www.imdb.com/name/nm3078932/?ref_=nv_sr_srsg_0_tt_7_nm_1_in_0_q_Lady%2520Gaga",
            "Ella Purnell": "https://www.imdb.com/name/nm3480246/",
            "Antony Starr": "https://www.imdb.com/name/nm1102278/?ref_=fn_al_nm_1",
            "Dakota Johnson": "https://www.imdb.com/name/nm0424848/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_Dakota%2520Johnson",
            "Tom Hiddleston": "https://www.imdb.com/name/nm1089991/?ref_=nv_sr_srsg_0_tt_2_nm_6_in_0_q_Tom%2520Hiddleston",
            "Sophia Di Martino": "https://www.imdb.com/name/nm1620545/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_Sophia%2520Di%2520Martino",
            "Winona Ryder": "https://www.imdb.com/name/nm0000213/?ref_=nv_sr_srsg_0_tt_2_nm_5_in_0_q_Winona%2520Ryder",
            "Monica Bellucci": "https://www.imdb.com/name/nm0000899/?ref_=nv_sr_srsg_0_tt_4_nm_4_in_0_q_Monica%2520Bellucci",
            "Willem Dafoe": "https://www.imdb.com/name/nm0000353/?ref_=nv_sr_srsg_0_tt_5_nm_3_in_0_q_Willem%2520Dafoe",
            "Sebastian Stan": "https://www.imdb.com/name/nm1659221/?ref_=nv_sr_srsg_0_tt_1_nm_7_in_0_q_Sebastian%2520Stan",
            "Morfydd Clark": "https://www.imdb.com/name/nm6077056/"
        }

        for name, imdb_link in actor_imdb_links.items():
            wiki_data = fetch_wikipedia_data(name)
            actors_top.append({
                "Name": name,
                "ProfileImage": wiki_data.get("ProfileImage"),
                "Summary": wiki_data.get("Summary"),
                "WikipediaLink": wiki_data.get("WikipediaLink"),
                "IMDbLink": imdb_link
            })

        serializer = ActorSerializer(actors_top, many=True)
        return Response({"actors": serializer.data}, status=status.HTTP_200_OK)

class PopularReleasesActors(APIView):
    """
    Аналогичный класс представления для актеров.
    """
    def get(self, request):
        actors_data = []
        actor_imdb_links = {
            "Aaron Taylor-Johnson": "https://www.imdb.com/name/nm1093951/?ref_=tt_cst_t_1",
            "Dwayne Johnson": "https://www.imdb.com/name/nm0425005/?ref_=tt_cst_t_2",
            "Ben Stiller": "https://www.imdb.com/name/nm0001774/?ref_=tt_cst_t_1",
            "Linda Cardellini": "https://www.imdb.com/name/nm0004802/?ref_=tt_cst_t_6",
            "Adam Driver": "https://www.imdb.com/name/nm3485845/?ref_=tt_cst_t_1",
            "Shia LaBeouf": "https://www.imdb.com/name/nm0479471/?ref_=tt_cst_t_5",
            "Laurence Fishburne": "https://www.imdb.com/name/nm0000401/?ref_=tt_cst_t_7",
            "Florence Pugh": "https://www.imdb.com/name/nm6073955/?ref_=tt_cst_t_1",
            "David Harbour": "https://www.imdb.com/name/nm1092086/?ref_=tt_cst_t_4",
            "Rachel Weisz": "https://www.imdb.com/name/nm0001838/?ref_=tt_cst_t_3",
            "Hugh Grant": "https://www.imdb.com/name/nm0000424/?ref_=tt_cst_t_1",
            "Harrison Ford": "https://www.imdb.com/name/nm0000148/?ref_=tt_cst_t_1",
            "Liv Tyler": "https://www.imdb.com/name/nm0000239/?ref_=tt_cst_t_3",
            "Anthony Mackie": "https://www.imdb.com/name/nm1107001/?ref_=tt_cst_t_5",
            "Tom Hardy": "https://www.imdb.com/name/nm0362766/?ref_=tt_cst_t_1",
            "Juno Temple": "https://www.imdb.com/name/nm1017334/?ref_=tt_cst_t_3"
        }

        for name, imdb_link in actor_imdb_links.items():
            wiki_data = fetch_wikipedia_data(name)
            actors_data.append({
                "Name": name,
                "ProfileImage": wiki_data.get("ProfileImage"),
                "Summary": wiki_data.get("Summary"),
                "WikipediaLink": wiki_data.get("WikipediaLink"),
                "IMDbLink": imdb_link
            })

        return Response({"actors": actors_data}, status=status.HTTP_200_OK)