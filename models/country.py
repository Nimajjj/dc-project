class Country:
    def __init__(self, id_country, iso_3166_1, country_name):  
        self.id_country = id_country
        self.iso_3166_1 = iso_3166_1
        self.country_name = country_name

    def __str__(self) -> str:
        return f"Country(id={self.id_country}, iso_3166_1={self.iso_3166_1}, name={self.country_name})"
