# models/movie_complete.py
from dal import DAL
from models.movie import Movie
from models.language import Language
from models.genre import Genre
from models.country import Country

class MovieComplete:
    def __init__(self, movie: Movie, genres: list, original_language: str, production_countries: list, spoken_languages: list) -> None:
        # movie general
        self.movie = movie
        self.original_language = original_language  # todo(nmj): move to movie.Movie class

        # format genres
        self.genres = []
        for genre in genres:
            self.genres.append(Genre(0, genre["name"]))

        # format production_countries
        self.production_countries = []
        for country in production_countries:
            self.production_countries.append(Country(
                0,
                country["iso_3166_1"],
                country["name"]
            ))

        # format spoken_languages
        self.spoken_languages = []
        for lang in spoken_languages:
            self.spoken_languages.append(Language(
                0, # auto
                lang["iso_639_1"],
                lang["name"],
                lang["english_name"]
            ))


    def InsertIntoDB(self) -> None:
        self._insertGenres()
        self._insertProductionCountries()
        self._insertSpokenLanguages()
        self._insertMovie()

        self._linkForeignKeys()


    # todo(nmj): check if link already exists
    # todo(nmj): replace all '"' char by '
    def _linkForeignKeys(self) -> None:
        dal = DAL()

        query = f"SELECT id_movie FROM movies WHERE title=\"{self.movie.title}\";"
        res = dal.Select(query)

        # if cannot find movie then return
        if (len(res) == 0):
            return

        id_movie = res[0][0]

        # link genres
        for genre in self.genres:
            query = f"SELECT id_genre FROM genres WHERE title=\"{genre.title}\";"
            res = dal.Select(query)
            if (len(res) == 0):
                return
            id_genre = res[0][0]

            query = "INSERT INTO genres_movies (id_movie, id_genre) VALUES (%s, %s)"
            dal.Insert(query, (id_movie, id_genre))

        # link countries
        for country in self.production_countries:
            query = f"SELECT id_country FROM countries WHERE iso_3166_1=\"{country.iso_3166_1}\";"
            res = dal.Select(query)
            if (len(res) == 0):
                return
            id_country = res[0][0]

            query = "INSERT INTO countries_movies (id_movie, id_country) VALUES (%s, %s)"
            dal.Insert(query, (id_movie, id_country))

        # link languages
        for language in self.spoken_languages:
            query = f"SELECT id_language FROM languages WHERE iso_639_1=\"{language.iso_639_1}\";"
            res = dal.Select(query)

            if (len(res) == 0):
                return
            id_language = res[0][0]

            query = "INSERT INTO movie_languages (id_movie, id_language) VALUES (%s, %s)"
            dal.Insert(query, (id_movie, id_language))


    def _insertMovie(self) -> None:
        dal = DAL()
        query = f"SELECT * FROM movies WHERE title=\"{self.movie.title}\";"
        res = dal.Select(query)

        # if movie already exists then return
        if (len(res) != 0):
            return

        query = "INSERT INTO cinema.movies (duration_min, original_title, imdb_id, title, overview, poster, release_date, visa_number, minimum_age, awards, id_distributor, original_laguage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (
            self.movie.duration_min,
            self.movie.original_title,
            self.movie.imdb_id,
            self.movie.title,
            self.movie.overview,
            self.movie.poster,
            self.movie.release_date,
            self.movie.visa_number,
            self.movie.minimum_age,
            self.movie.awards,
            self.movie.id_distributor,
            self.original_language
        )
        dal.Insert(query, values)


    def _insertSpokenLanguages(self) -> None:
        dal = DAL()
        for language in self.spoken_languages:
            query = f"SELECT * FROM languages WHERE iso_639_1=\"{language.iso_639_1}\";"
            res = dal.Select(query)

            # if language already exists then continue
            if (len(res) != 0):
                continue

            # else insert new 
            query = f"INSERT INTO languages (iso_639_1, language_name, english_name) VALUES (%s, %s, %s);"
            dal.Insert(query, (language.iso_639_1, language.language_name, language.english_name))
        

    def _insertProductionCountries(self) -> None:
        dal = DAL()
        for country in self.production_countries:
            query = f"SELECT * FROM countries WHERE iso_3166_1=\"{country.iso_3166_1}\";"
            res = dal.Select(query)

            # if country already exists then continue
            if (len(res) != 0):
                continue

            # else insert new 
            query = f"INSERT INTO countries (iso_3166_1, country_name) VALUES (%s, %s);"
            dal.Insert(query, (country.iso_3166_1, country.country_name))


    def _insertGenres(self) -> None:
        dal = DAL()
        for genre in self.genres:
            query = f"SELECT * FROM genres WHERE title=\"{genre.title}\";"
            res = dal.Select(query)

            # if genre already exists then continue
            if (len(res) != 0):
                continue

            # else insert new
            query = f"INSERT INTO genres (title) VALUES (%s);"
            dal.Insert(query, (genre.title,))
