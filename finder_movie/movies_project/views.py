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
                    "imdbID": movie_data.get('imdbID'),
                    "Actors": movie_data.get('Actors')
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
                    "imdbID": movie_data.get('imdbID'),
                    "Actors": movie_data.get('Actors')
                })

        return Response({"movies": movies_top}, status=status.HTTP_200_OK)


class TopActors(APIView):
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
            "Morfydd Clark": "https://www.imdb.com/name/nm6077056/?ref_=nv_sr_srsg_0_tt_0_nm_1_in_0_q_Morfydd%2520Clark",
            "Antony Starr": "https://www.imdb.com/name/nm1102278/?ref_=fn_al_nm_1",
            "Dakota Johnson": "https://www.imdb.com/name/nm0424848/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_Dakota%2520Johnson",
            "Tom Hiddleston": "https://www.imdb.com/name/nm1089991/?ref_=nv_sr_srsg_0_tt_2_nm_6_in_0_q_Tom%2520Hiddleston",
            "Sophia Di Martino": "https://www.imdb.com/name/nm1620545/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_Sophia%2520Di%2520Martino",
            "Winona Ryder": "https://www.imdb.com/name/nm0000213/?ref_=nv_sr_srsg_0_tt_2_nm_5_in_0_q_Winona%2520Ryder",
            "Monica Bellucci": "https://www.imdb.com/name/nm0000899/?ref_=nv_sr_srsg_0_tt_4_nm_4_in_0_q_Monica%2520Bellucci",
            "Willem Dafoe": "https://www.imdb.com/name/nm0000353/?ref_=nv_sr_srsg_0_tt_5_nm_3_in_0_q_Willem%2520Dafoe",
            "Sebastian Stan": "https://www.imdb.com/name/nm1659221/?ref_=nv_sr_srsg_0_tt_1_nm_7_in_0_q_Sebastian%2520Stan",
            "Millie Bobby Brown": "https://www.imdb.com/name/nm5611121/?ref_=nv_sr_srsg_0_tt_4_nm_2_in_0_q_Millie%2520Bobby%2520Brown"
        }

        actor_names = [
            "Cristin Milioti", "Colin Farrell", "Margaret Qualley", "Demi Moore", "Ryan Reynolds",
            "Cailee Spaeny", "Kathryn Hahn", "Aubrey Plaza", "Robert Pattinson", "Anya Taylor-Joy",
            "Zoë Kravitz", "Chris Hemsworth", "Joaquin Phoenix", "Lady Gaga", "Morfydd Clark",
            "Antony Starr", "Dakota Johnson", "Tom Hiddleston", "Sophia Di Martino", "Winona Ryder",
            "Monica Bellucci", "Willem Dafoe", "Sebastian Stan", "Millie Bobby Brown"
        ]

        for name in actor_names:
            wiki_url = "https://en.wikipedia.org/w/api.php"
            wiki_params = {
                "action": "query",
                "format": "json",
                "titles": name,
                "prop": "pageimages|extracts",
                "exintro": True,
                "explaintext": True,
                "piprop": "original",
            }
            wiki_response = requests.get(wiki_url, params=wiki_params)
            wiki_data = wiki_response.json()

            profile_image = None
            summary = None
            if wiki_response.status_code == 200:
                pages = wiki_data.get('query', {}).get('pages', {})
                for page_id, page in pages.items():
                    if page_id != "-1":
                        profile_image = page.get("original", {}).get("source")
                        summary = page.get("extract")

            imdb_link = actor_imdb_links.get(name)

            actors_top.append({
                "Name": name,
                "ProfileImage": profile_image,
                "Summary": summary,
                "WikipediaLink": f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}",
                "IMDbLink": imdb_link
            })

        return Response({"actors": actors_top}, status=200)