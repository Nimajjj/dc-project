# Copyright (C) 2023 Borello Benjamin
# models/country.py
from dal import DAL
# todo(nmj): Handle english / french country name from TMDB and FirCinema

class Country:
    def __init__(self, iso_3166_1, country_name):  
        self.id_country = 0
        self.iso_3166_1 = iso_3166_1
        self.country_name = country_name

    def __str__(self) -> str:
        return f"Country(id={self.id_country}, iso_3166_1={self.iso_3166_1}, name={self.country_name})"

    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM countries WHERE country_name = %s"
        res = DAL().Select(query, (self.country_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO countries (iso_3166_1, country_name) VALUES (%s, %s);"
        DAL().Insert(query, (self.iso_3166_1, self.country_name))


    def LinkToMovie(self, id_movie: int) -> None:
        # Check if item exists
        query = "SELECT id_country FROM countries WHERE country_name = %s"
        res = DAL().Select(query, (self.country_name,))
        if (len(res) == 0):
            return

        # Set id
        self.id_country = res[0][0]

        # Check if link already exists
        query = "SELECT * FROM countries_movies WHERE id_movie = %s AND id_country = %s"
        res = DAL().Select(query, (id_movie, self.id_country))
        if (len(res) != 0):
            return

        # Insert link
        query = "INSERT INTO countries_movies (id_movie, id_country) VALUES (%s, %s)"
        DAL().Insert(query, (id_movie, self.id_country))
