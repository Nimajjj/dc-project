# models/country.py
from dal import DAL

class Country:
    def __init__(self, id_country, iso_3166_1, country_name):  
        self.id_country = id_country
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
