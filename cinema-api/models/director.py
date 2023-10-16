# models/director.py
from dal import DAL

class Director:
    def __init__(self, id_director, director_name):    
        self.id_director = id_director
        self.director_name = director_name

    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM directors WHERE director_name = %s"
        res = DAL().Select(query, (self.director_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO directors (director_name) VALUES (%s);"
        DAL().Insert(query, (self.director_name,))

