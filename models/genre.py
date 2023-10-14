class Genre:
    def __init__(self, id_genre, title):
        self.id_genre = id_genre 
        self.title = title

    def __str__(self) -> str:
        return f"Genre(id={self.id_genre}, title={self.title})"
