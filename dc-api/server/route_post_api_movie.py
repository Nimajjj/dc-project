# Copyright (C) 2023 Borello Benjamin
# server/route_post_api_movie.py
from models.actor import Actor
from models.country import Country
from models.director import Director
from models.distributor import Distributor
from models.genre import Genre
from models.movie import Movie
from models.language import Language
from models.writer import Writer


def ApplyData(data) -> None:
    # Creating Movie object
    m = Movie()
    m.src_type = "FirCinema"
    m.title = data["title"]
    m.duration = data["duration"]
    m.overview = data["overview"]
    m.thumnail = data["thumbnail"]
    m.release_date = data["date"]
    m.visa = data["visa"]
    m.distributor = Distributor(data["distributor"])

    for title in data["language"]:
        m.languages.append(Language("iso_639_1", title, title))

    for title in data["country"]:
        m.countries.append(Country("iso_3166_1", title))

    for title in data["genres"]:
        m.genres.append(Genre(title))

    for title in data["actors"]:
        m.actors.append(Actor(title))

    for title in data["directors"]:
        m.directors.append(Director(title))

    for title in data["writers"]:
        m.writers.append(Writer(title))

    if (m.IsInDatabase()):
        print("[DC-api] ['POST' /api/movie] Updating movie data in database...")
        db_response = m.UpdateInDB()
        log_message = "Movie successfuly updated in database." if (db_response > 0) else "Error while updating movie from database."
        print(f"[DC-api] ['POST' /api/movie] {log_message}")
    else:
        print("[DC-api] ['POST' /api/movie] Adding movie to database...")
        db_response = m.InsertIntoDB()
        log_message = "Movie successfuly inserted in database." if (db_response > 0) else "Error while inserting movie into database."
        print(f"[DC-api] ['POST' /api/movie] {log_message}")
        

