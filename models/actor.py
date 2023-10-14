# models/actor.py

from dal import DAL

class Actor:  
    def __init__(self, id_actor: int, actor_name: str):
        self.id_actor = id_actor
        self.actor_name = actor_name


    @staticmethod
    def SelectById(id: str|int):
        dal = DAL()
        result = dal.SelectSingleRow("SELECT * FROM actors WHERE id_actor = " + str(id))


        if (len(result) == 0):
            return None

        return Actor(
                result["id_actor"],
                result["actor_name"]
                )


    def __str__(self) -> str:
        return "Actor(id_actor={0}, actor_name=\"{1}\")".format(self.id_actor, self.actor_name)

    def IsValid(self) -> bool:
        return (self.id_actor != -1)

