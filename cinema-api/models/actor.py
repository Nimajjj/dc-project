# models/actor.py
from dal import DAL

class Actor:  
    def __init__(self, id_actor: int, actor_name: str):
        self.id_actor = id_actor
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
