# models/distributor.py
from dal import DAL

class Distributor:
    def __init__(self, distributor_name):
        self.id_distributor = 0
        self.distributor_name = distributor_name

    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM distributors WHERE distributor_name = %s"
        res = DAL().Select(query, (self.distributor_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO distributors (distributor_name) VALUES (%s);"
        DAL().Insert(query, (self.distributor_name,))

    def GetID(self) -> int:
        query = "SELECT id_distributor FROM distributors WHERE distributor_name = %s"
        res = DAL().Select(query, (self.distributor_name,))
        if (len(res) == 0):
            return -1

        return res[0][0]
