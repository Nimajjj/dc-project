# models/writer.py
from dal import DAL

class Writer:  
    def __init__(self, id_writer: int, writer_name: str):
        self.id_writer = id_writer
        self.writer_name = writer_name


    def __str__(self) -> str:
        return "Writer(id_writer={0}, writer_name=\"{1}\")".format(self.id_writer, self.writer_name)


    def InsertIntoDB(self) -> None:
        query = "SELECT * FROM writers WHERE writer_name = %s"
        res = DAL().Select(query, (self.writer_name,))
        if (len(res) != 0):
            return

        query = "INSERT INTO writers (writer_name) VALUES (%s);"
        DAL().Insert(query, (self.writer_name,))

