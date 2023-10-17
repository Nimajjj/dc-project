# main.py
import tmdb
from api import server
from models.movie import Movie

id = 961084

if __name__ == "__main__":
    # Start DC-api server
    server.RunServer()

