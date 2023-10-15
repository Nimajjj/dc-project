# models/movie.py

from dal import DAL

class Movie:
    def __init__(self, id_movie, duration_min, original_title, imdb_id, title, overview, poster, release_date, visa_number, minimum_age, awards, id_distributor, id_language):
        self.id_movie = id_movie
        self.duration_min = duration_min
        self.original_title = original_title
        self.imdb_id = imdb_id
        self.title = title
        self.overview = overview
        self.poster = poster
        self.release_date = release_date
        self.visa_number = visa_number 
        self.minimum_age = minimum_age
        self.awards = awards
        self.id_distributor = id_distributor
        self.id_language = id_language


    @staticmethod
    def SelectById(id: str|int):
        dal = DAL()
        result = dal.SelectSingleRow("SELECT * FROM movies WHERE id_movie = " + str(id))

        if (len(result) == 0):
            return None

        return Movie(
                result["id_movie"],
                result["duration_min"],
                result["original_title"],
                result["imdb_id"],
                result["title"],
                result["overview"],
                result["poster"],
                result["release_date"],
                result["visa_number"],
                result["minimum_age"],
                result["awards"],
                result["id_distributor"],
                result["id_language"]
                )


    def __str__(self):
        return f"Movie(id_movie={self.id_movie},\n duration_min={self.duration_min},\n original_title={self.original_title},\n imdb_id={self.imdb_id},\n title={self.title},\n overview={self.overview},\n poster={self.poster},\n release_date={self.release_date},\n visa_number={self.visa_number},\n minimum_age={self.minimum_age},\n awards={self.awards},\n id_distributor={self.id_distributor},\n id_language={self.id_language}\n)"
        

    def IsValid(self) -> bool:
        return (self.id_movie != -1)
