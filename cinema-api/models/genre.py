# models/genre.py
from dal import DAL

class Genre:
    def __init__(self, id_genre, title):
        self.id_genre = id_genre 
        self.title = title


    def __str__(self) -> str:
        return f"Genre(id={self.id_genre}, title={self.title})"


    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM genres WHERE title = %s"
        res = DAL().Select(query, (self.title,))
        if (len(res) != 0):
            return

        query = "INSERT INTO genres (title) VALUES (%s)"
        DAL().Insert(query, (self.title,))
