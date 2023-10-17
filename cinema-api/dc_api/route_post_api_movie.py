# dc_api/route_post_api_movie.py
from dal import DAL
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

    # Verify is movie already exists in db
    dal = DAL()
    query = "SELECT id_movie, release_date FROM movies WHERE title = %s"
    values = (m.title,)
    results = dal.Select(query, values)

    # todo(nmj): double check movie title AND release date
    # to ensure that it is not an other movie with the same title
    if (results):
        print("[DC-api] ['POST' /api/movie] Movie already exists in database")
        print("[DC-api] ['POST' /api/movie] Updating movie data in database...")
        # Update database entry
    else:
        # Append database entry
        # todo(nmj): Double check on TMDB api side that an allocine 
        # movie not already exists
        print("[DC-api] ['POST' /api/movie] Movie does not exists in database")
        print("[DC-api] ['POST' /api/movie] Adding movie to database...")
        print(m.InsertIntoDB())
        

