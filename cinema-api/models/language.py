# models/languages.py
from dal import DAL

class Language:    
    def __init__(self, id_language, iso_639_1, language_name, english_name):
        self.id_language = id_language
        self.iso_639_1 = iso_639_1
        self.language_name = language_name
        self.english_name = english_name

    def __str__(self) -> str:
        return f"Language(id={self.id_language}, iso_639_1={self.iso_639_1}, language_name={self.language_name}, english_name={self.english_name})"


    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM languages WHERE language_name = %s"
        res = DAL().Select(query, (self.language_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO languages (iso_639_1, language_name, english_name) VALUES (%s, %s, %s);"
        DAL().Insert(query, (self.iso_639_1, self.language_name, self.english_name))
