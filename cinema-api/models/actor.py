# models/actor.py
from dal import DAL

class Actor:  
    def __init__(self, actor_name: str):
        self.id_actor = 0
        self.actor_name = actor_name


    def __str__(self) -> str:
        return "Actor(id_actor={0}, actor_name=\"{1}\")".format(self.id_actor, self.actor_name)

    def IsValid(self) -> bool:
        return (self.id_actor != -1)

    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM actors WHERE actor_name = %s"
        res = DAL().Select(query, (self.actor_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO actors (actor_name) VALUES (%s);"
        DAL().Insert(query, (self.actor_name,))


    def LinkToMovie(self, id_movie: int) -> None:
        # Check if item exists
        query = "SELECT id_actor FROM actors WHERE actor_name = %s"
        res = DAL().Select(query, (self.actor_name,))
        if (len(res) == 0):
            return

        # Set id
        self.id_actor = res[0][0]

        # Check if link already exists
        query = "SELECT * FROM actors_movies WHERE id_movie = %s AND id_actor = %s"
        res = DAL().Select(query, (id_movie, self.id_actor))
        if (len(res) != 0):
            return

        # Insert link
        query = "INSERT INTO actors_movies (id_movie, id_actor) VALUES (%s, %s)"
        DAL().Insert(query, (id_movie, self.id_actor))
