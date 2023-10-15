# tmdb.py
import requests
from models.movie import Movie
from models.movie_complete import MovieComplete

url = "https://api.themoviedb.org/3/movie/{movie_id}?language=fr-FR"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ODkxOWQxOGFjMTE2MDg1ZTQ4ZjNiZTRjMmZkZTRiYyIsInN1YiI6IjY0MGM1MjQwZTE4ZTNmMDgxNmMyN2RjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.e-SdYrD-u4jWvetmiwCE0lN9zSRjRAmpIlKDkgDIIB8"
}

def RequestMovie(id: int) -> Movie|None:
    # request api
    response = requests.get(url.format(movie_id = id), headers=headers).json()

    # verify if movie with given id exists
    if not "title" in response.keys():
        return None

    # get all relavent datas
    genres = response["genres"]
    imdb_id = response["imdb_id"]
    ori_lang = response["original_language"]
    ori_title = response["original_title"]
    overview = response["overview"]
    poster_path = response["poster_path"]
    prod_countries = response["production_countries"]
    release_date = response["release_date"]
    spoken_lang = response["spoken_languages"]
    title = response["title"]
    duration = response["runtime"]

    # make movie object
    movie = Movie(
        None,  # auto
        duration,
        ori_title,
        imdb_id,
        title,
        overview,
        poster_path,
        release_date,
        None,  # manual input
        None,  # manual input
        None, # manual input
        None,  # scrap
        None   # fk
    )

    return MovieComplete(movie, genres, ori_lang, prod_countries, spoken_lang)

