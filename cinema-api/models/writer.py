# Copyright (C) 2023 Borello Benjamin
# models/writer.py
from dal import DAL

class Writer:  
    def __init__(self, writer_name: str):
        self.id_writer = 0
        self.writer_name = writer_name


    def __str__(self) -> str:
        return "Writer(id_writer={0}, writer_name=\"{1}\")".format(self.id_writer, self.writer_name)


    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM writers WHERE writer_name = %s"
        res = DAL().Select(query, (self.writer_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO writers (writer_name) VALUES (%s);"
        DAL().Insert(query, (self.writer_name,))


    def LinkToMovie(self, id_movie: int) -> None:
        # Check if item exists
        query = "SELECT id_writer FROM writers WHERE writer_name = %s"
        res = DAL().Select(query, (self.writer_name,))
        if (len(res) == 0):
            return

        # Set id
        self.id_writer = res[0][0]

        # Check if link already exists
        query = "SELECT * FROM movies_writers WHERE id_movie = %s AND id_writer = %s"
        res = DAL().Select(query, (id_movie, self.id_writer))
        if (len(res) != 0):
            return

        # Insert link
        query = "INSERT INTO movies_writers (id_movie, id_writer) VALUES (%s, %s)"
        DAL().Insert(query, (id_movie, self.id_writer))
