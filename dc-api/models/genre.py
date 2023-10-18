# Copyright (C) 2023 Borello Benjamin
# models/genre.py
from dal import DAL

class Genre:
    def __init__(self, title):
        self.id_genre = 0 
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


    def LinkToMovie(self, id_movie: int) -> None:
        # Check if item exists
        query = "SELECT id_genre FROM genres WHERE title = %s"
        res = DAL().Select(query, (self.title,))
        if (len(res) == 0):
            return

        # Set id
        self.id_genre = res[0][0]

        # Check if link already exists
        query = "SELECT * FROM genres_movies WHERE id_movie = %s AND id_genre = %s"
        res = DAL().Select(query, (id_movie, self.id_genre))
        if (len(res) != 0):
            return

        # Insert link
        query = "INSERT INTO genres_movies (id_movie, id_genre) VALUES (%s, %s)"
        DAL().Insert(query, (id_movie, self.id_genre))
