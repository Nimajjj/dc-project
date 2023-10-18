# Copyright (C) 2023 Borello Benjamin
# models/movie.py
import re
import locale
import datetime
from dal import DAL
from models.distributor import Distributor


class  Movie:
    def __init__(self, *args) -> None:
        self.dal = DAL()
        self.src_type = "n/a"

        self.id_movie = 0   # 0 = n/a; -1 = error while inserting movie;
        self.imdb_id = None
        self.visa = None
        self.minimum_age = None
        self.awards = None
        self.distributor = None
        self.title = ""
        self.original_title = ""
        self.duration = ""
        self.overview = ""
        self.thumnail = ""
        self.release_date = ""
        self.language = ""
        self.languages = [] 
        self.countries = [] 
        self.genres = [] 
        self.actors = [] 
        self.directors = [] 
        self.writers = [] 

        if (len(args) == 0):
            return


    def __str__(self) -> str:
        return f"Movie(id_movie={self.id_movie},\n" \
                f"imdb_id={self.imdb_id},\n" \
                f"title={self.title},\n" \
                f"original_title={self.original_title},\n" \
                f"duration={self.duration},\n" \
                f"overview={self.overview},\n" \
                f"thumnail={self.thumnail},\n" \
                f"release_date={self.release_date},\n" \
                f"visa={self.visa},\n" \
                f"distributor={self.distributor},\n" \
                f"language={self.language},\n" \
                f"languages={self.languages},\n" \
                f"countries={self.countries},\n" \
                f"genres={self.genres},\n" \
                f"actors={self.actors},\n" \
                f"directors={self.directors},\n" \
                f"writers={self.writers},\n" \
                f"minimum_age={self.minimum_age},\n" \
                f"awards={self.awards})"


    # todo(nmj): double check movie title AND release date
    # to ensure that it is not an other movie with the same title
    def IsInDatabase(self) -> bool:
        query = "SELECT id_movie FROM movies WHERE title=%s;"
        res = DAL().Select(query, (self.title,))
        return (len(res) != 0)

    def GetDBMovieID(self) -> int:
        query = "SELECT id_movie FROM movies WHERE title=%s;"
        res = DAL().Select(query, (self.title,))
        if (len(res) == 0):
            # movie insertion failed
            return -1

        return res[0][0]

    
    def UpdateInDB(self) -> int:
        if (not self.IsInDatabase()):
            return -1

        if (self.src_type == "n/a"):
            return -2

        if (self.src_type == "FirCinema"):
            print("[DC-api] Updating db movie from FirCinema source")
            self.id_movie = self.GetDBMovieID()
            self._updateFromFCSource()

        if (self.src_type == "TMDB"):
            print("[DC-api] Updating db movie from TMDB source")
            self.id_movie = self.GetDBMovieID()
            self._updateFromTMDBSource()

        return self.id_movie


    def _updateFromTMDBSource(self) -> None:
        # Just in case, anyway ther is securities which avoid duplicated entries
        self._insertLanguages()
        self._insertCountries()

        self._linkLanguages()
        self._linkCountries()

        query = "UPDATE movies SET original_title = %s, imdb_id = %s, original_laguage = %s WHERE id_movie = %s"
        values = (self.original_title, self.imdb_id, self.language, self.id_movie)
        DAL().Execute(query, values, True)


    def _updateFromFCSource(self) -> None:
        # Just in case, anyway ther is securities which avoid duplicated entries
        self._insertActors()
        self._insertDirectors()
        self._insertWriters()

        self._linkActors()
        self._linkDirectors()
        self._linkWriters()

        id_distributor = self._insertDistributor()
        query = "UPDATE movies SET id_distributor = %s WHERE id_movie = %s"
        values = (id_distributor, self.id_movie)
        DAL().Execute(query, values, True)


    
    def InsertIntoDB(self) -> int:
        # avoid insertion of unprepared movie
        if (self.src_type == "n/a"):
            return -2

        if (self.src_type == "FirCinema"):
            # format duration from "1h 34"(str) to duration in minutes(int)
            match = re.match(r"(\d+)h (\d+)min", self.duration)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                self.duration = hours * 60 + minutes

            # format release_date from "dd monthName year"(str) to date "YYYY-MM-DD"(str)
            locale.setlocale(locale.LC_TIME, 'fr_FR')
            date = datetime.datetime.strptime(self.release_date, "%d %B %Y")
            self.release_date = date.strftime("%Y-%m-%d")

        if (self.src_type == "TMDB"):
            if (self.IsInDatabase):
                print("Movie already exists in db, pass from inserting to updating...")
                return self.UpdateInDB()

        self._insertMainTables()
        self._linkForeignKeys()
        return self.id_movie


    # privates
    # general
    def _insertMainTables(self) -> None:
        self._insertGenres()
        self._insertLanguages()
        self._insertCountries()
        self._insertActors()
        self._insertDirectors()
        self._insertWriters()
        id_distributor = self._insertDistributor()
        self.id_movie = self._insertMovie(id_distributor)


    def _linkForeignKeys(self) -> None:
        if (self.id_movie <= 0 or not self.IsInDatabase()):
            return

        self._linkGenres()
        self._linkLanguages()
        self._linkCountries()
        self._linkActors()
        self._linkDirectors()
        self._linkWriters()


    # insert
    def _insertGenres(self) -> None:
        if (len(self.genres) == 0):
            return

        for genre in self.genres:
            genre.InsertIntoDB()

    def _insertLanguages(self) -> None:
        if (len(self.languages) == 0):
            return

        for language in self.languages:
            # todo(nmj): create function to get iso_639_1 from french language name
            language.InsertIntoDB()

    def _insertCountries(self) -> None:
        if (len(self.countries) == 0):
            return

        for country in self.countries:
            # todo(nmj): create function to get iso_3166_1 from french country name
            country.InsertIntoDB()

    def _insertActors(self) -> None:
        if (len(self.actors) == 0):
            return

        for actor in self.actors:
            actor.InsertIntoDB()

    def _insertDirectors(self) -> None:
        if (len(self.directors) == 0):
            return

        for director in self.directors:
            director.InsertIntoDB()

    def _insertWriters(self) -> None:
        if (len(self.writers) == 0):
            return

        for writer in self.writers:
            writer.InsertIntoDB()

    def _insertDistributor(self) -> int|None:
        if (not self.distributor):
            return None

        self.distributor.InsertIntoDB()
        return self.distributor.GetID()


    def _insertMovie(self, id_distributor: int|None) -> int:
        if (self.IsInDatabase()):
            query = "SELECT id_movie FROM movies WHERE title=%s;"
            res = DAL().Select(query, (self.title,))
            if (len(res) != 0):
                return res[0][0] 

        query = (
            "INSERT INTO movies " 
            "(duration_min, original_title, imdb_id, title, overview, poster, release_date, visa_number, minimum_age, awards, id_distributor, original_laguage)"
            "VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        values = (
            self.duration, 
            self.original_title,
            self.imdb_id,
            self.title,
            self.overview, 
            self.thumnail, 
            self.release_date, 
            self.visa, 
            self.minimum_age,
            self.awards,
            id_distributor,
            self.language
        )

        DAL().Insert(query, values)
        return self.GetDBMovieID()


    # link
    def _linkGenres(self) -> None:
        for genre in self.genres:
            genre.LinkToMovie(self.id_movie)

    def _linkLanguages(self) -> None:
        for language in self.languages:
            language.LinkToMovie(self.id_movie)

    def _linkCountries(self) -> None:
        for country in self.countries:
            country.LinkToMovie(self.id_movie)

    def _linkActors(self) -> None:
        for actor in self.actors:
            actor.LinkToMovie(self.id_movie)

    def _linkDirectors(self) -> None:
        for director in self.directors:
            director.LinkToMovie(self.id_movie)

    def _linkWriters(self) -> None:
        for writer in self.writers:
            writer.LinkToMovie(self.id_movie)
