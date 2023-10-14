class Language:    
    def __init__(self, id_language, iso_639_1, language_name, english_name):
        self.id_language = id_language
        self.iso_639_1 = iso_639_1
        self.language_name = language_name
        self.english_name = english_name

    def __str__(self) -> str:
        return f"Language(id={self.id_language}, iso_639_1={self.iso_639_1}, language_name={self.language_name}, english_name={self.english_name})"
