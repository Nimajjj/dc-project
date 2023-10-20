# Copyright (C) 2023 Borello Benjamin
# tmdb.py
from dotenv import dotenv_values
import requests
from models.language import Language
from models.movie import Movie
from models.genre import Genre
from models.country import Country
from models.language import Language

url = "https://api.themoviedb.org/3/movie/{movie_id}?language=fr-FR"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {dotenv_values('TMDB_API_KEY')}"
}

def RequestMovie(id: int) -> Movie|None:
    response = requests.get(url.format(movie_id = id), headers=headers).json()

    # todo(nmj): verify data integrity
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
    
    # Always assign src_type in last in case one of the previous assignment fails
    movie.src_type = "TMDB"
    return movie
