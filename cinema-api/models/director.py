# models/director.py
from dal import DAL

class Director:
    def __init__(self, director_name):    
        self.id_director = 0
        self.director_name = director_name

    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM directors WHERE director_name = %s"
        res = DAL().Select(query, (self.director_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO directors (director_name) VALUES (%s);"
        DAL().Insert(query, (self.director_name,))


    def LinkToMovie(self, id_movie: int) -> None:
        # Check if item exists
        query = "SELECT id_director FROM directors WHERE director_name = %s"
        res = DAL().Select(query, (self.director_name,))
        if (len(res) == 0):
            return

        # Set id
        self.id_director = res[0][0]

        # Check if link already exists
        query = "SELECT * FROM directors_movies WHERE id_movie = %s AND id_director = %s"
        res = DAL().Select(query, (id_movie, self.id_director))
        if (len(res) != 0):
            return

        # Insert link
        query = "INSERT INTO directors_movies (id_movie, id_director) VALUES (%s, %s)"
        DAL().Insert(query, (id_movie, self.id_director))
