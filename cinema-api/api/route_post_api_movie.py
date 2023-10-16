# api/route_post_api_movie.py
from dal import DAL
from models import movie
from models import movie_allo


def ApplyData(data) -> None:
    # Creating movie_allo class
    m = movie_allo.MovieAllo()
    m.title = data["title"]
    m.duration = data["duration"]
    m.overview = data["overview"]
    m.thumnail = data["thumbnail"]
    m.release_date = data["date"]
    m.visa = data["visa"]
    m.distributor = data["distributor"]
    m.languages = data["language"]
    m.countries = data["country"]
    m.genres = data["genres"]   
    m.actors = data["actors"]  
    m.directors = data["directors"]
    m.writers = data["writers"]   

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
        m.InsertIntoDB()
        

