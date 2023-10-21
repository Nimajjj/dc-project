# Copyright (C) 2023 Borello Benjamin
# server/route_get_movie.py

from typing import Dict
from dal import DAL
from models.movie import Movie


def GetMovie(id_movie: int, option: str) -> Dict :
    movie: Movie|None = None

    if (option == "minimal"):
        movie = Movie.SelectMovieMinimal(id_movie)

    if (option == "details"):
        movie = Movie.SelectMovieDetails(id_movie)

    return movie
