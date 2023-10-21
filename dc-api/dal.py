# Copyright (C) 2023 Borello Benjamin
# dal.py

# Singleton class for Database Abstraction Layer
from dotenv import dotenv_values, load_dotenv
import mysql.connector
from mysql.connector import cursor

class DAL():
    # Singleton snippet
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DAL, cls).__new__(cls)
        return cls.instance


    # Constructor
    # tofix(nmj): wtf... dotenv just don't works anymore ...
    def __init__(self) -> None:
        load_dotenv()
        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "cinema" 
        )


    def Select(self, query: str, values: tuple, debug: bool = False) -> list:
        if (debug):
            print(f"[DAL] {query} | {values}")

        cursor = self.db.cursor()
        cursor.execute(query, self._prepareValues(values))
        results = cursor.fetchall()
        return results


    def SelectSingleRow(self, query: str, debug: bool = False) -> dict|None:
        if (debug):
            print(f"[DAL] {query}")
        cursor = self.db.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        if (len(results) == 0):
            return None 

        columns = cursor.column_names
        dict_result = {} 
        
        for idx, value in enumerate(results[0]):
            dict_result[columns[idx]] = value

        return dict_result


    def Insert(self, query: str, values, debug: bool = False) -> None:
        if (debug):
            print(f"[DAL] {query} | {values}")
        cursor = self.db.cursor()
        cursor.execute(query, self._prepareValues(values))
        self.db.commit()


    def Execute(self, query: str, values, debug: bool = False) -> None:
        if (debug):
            print(f"[DAL] {query} | {values}")
        cursor = self.db.cursor()
        cursor.execute(query, self._prepareValues(values))
        self.db.commit()


    # privates
    def _prepareValues(self, values: tuple) -> tuple:
        listValues = []

        for value in values:
            if (isinstance(value, str)):
                listValues.append(value.replace("\"", "'"))
                continue
            listValues.append(value)

        return tuple(listValues)
    
