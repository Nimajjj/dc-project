# models/movie_allo.py
import re
import locale
import datetime
from dal import DAL
from models.language import Language
from models.genre import Genre
from models.country import Country
from models.actor import Actor
from models.director import Director
from models.writer import Writer
from models.distributor import Distributor


class MovieAllo:
    def __init__(self, *args) -> None:
        self.dal = DAL()

        self.title = ""
        self.duration = ""
        self.overview = ""
        self.thumnail = ""
        self.release_date = ""
        self.visa = ""
        self.distributor = ""
        self.languages = [] 
        self.countries = [] 
        self.genres = [] 
        self.actors = [] 
        self.directors = [] 
        self.writers = [] 

        if (len(args) == 0):
            return


    def ValuesAsTuple(self) -> tuple:
        return ()


    def InsertIntoDB(self) -> None:
        # self.duration from "Hh MM" (str) to minutes (int)
        match = re.match(r"(\d+)h (\d+)min", self.duration)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            self.duration = hours * 60 + minutes

        # self.release_date from "dd monthName year" (str) to date "YYY-MM-DD" (str)
        locale.setlocale(locale.LC_TIME, 'fr_FR')
        date = datetime.datetime.strptime(self.release_date, "%d %B %Y")
        self.release_date = date.strftime("%Y-%m-%d")

        self._insertMainTables()
        self._linkForeignKeys()


    # privates
    def _insertMainTables(self) -> None:
        self._insertGenres()
        self._insertLanguages()
        self._insertCountries()
        self._insertActors()
        self._insertDirectors()
        self._insertWriters()
        self.id_distributor = self._insertDistributor()
        self._insertMovie()


    def _linkForeignKeys(self) -> None:
        pass


    # insert
    def _insertGenres(self) -> None:
        for title in self.genres:
            Genre(0, title).InsertIntoDB()

    def _insertLanguages(self) -> None:
        for title in self.languages:
            # todo(nmj): create function to get iso_639_1 from french language name
            Language(0, "iso_639_1", title, "english_name")

    def _insertCountries(self) -> None:
        for title in self.countries:
            # todo(nmj): create function to get iso_3166_1 from french country name
            Country(0, "iso_3166_1", title).InsertIntoDB()

    def _insertActors(self) -> None:
        for actor in self.actors:
            Actor(0, actor).InsertIntoDB()

    def _insertDirectors(self) -> None:
        for director in self.directors:
            Director(0, director).InsertIntoDB()

    def _insertWriters(self) -> None:
        for writer in self.writers:
            Writer(0, writer).InsertIntoDB()

    def _insertDistributor(self) -> int:
        d = Distributor(0, self.distributor)
        d.InsertIntoDB()
        return d.GetID()

    def _insertMovie(self) -> None:
        query = "SELECT id_movie FROM movies WHERE title=%s;"
        res = DAL().Select(query, (self.title,))
        if (len(res) != 0):
            return

        query = "INSERT INTO movies (duration_min, overview, title, poster, release_date, visa_number, id_distributor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.duration, self.overview, self.title, self.thumnail, self.release_date, self.visa, self.id_distributor)
        DAL().Insert(query, values)
