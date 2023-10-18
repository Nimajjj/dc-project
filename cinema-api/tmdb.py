# Copyright (C) 2023 Borello Benjamin
# tmdb.py
import requests
from models.language import Language
from models.movie import Movie
from models.genre import Genre
from models.country import Country
from models.language import Language

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

    movie = Movie()

    movie.imdb_id = response["imdb_id"]
    movie.language = response["original_language"]
    movie.original_title = response["original_title"]
    movie.overview = response["overview"]
    movie.thumnail = response["poster_path"]
    movie.release_date = response["release_date"]
    movie.title = response["title"]
    movie.duration = response["runtime"]

    genres = response["genres"]
    for genre in genres:
        movie.genres.append(Genre(genre["name"]))

    countries = response["production_countries"]
    for country in countries:
        movie.countries.append(Country(
            country["iso_3166_1"], 
            country["name"]
        ))

    languages = response["spoken_languages"]
    for language in languages:
        movie.languages.append(Language(
            language["iso_639_1"],
            language["name"],
            language["english_name"],
        ))
    
    # Always assign src_type in last in case one of the previous assignment fail
    movie.src_type = "TMDB"
    return movie
