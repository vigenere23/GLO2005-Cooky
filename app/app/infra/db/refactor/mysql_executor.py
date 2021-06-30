from typing import Any
from mysql.connector.cursor import CursorBase

class MySQLExecutor:
    def __init__(self, cursor: CursorBase):
        self.__cursor: cursor

    def find(self, query, data=None) -> Any:
        self.__cursor.execute(query, data)
        result = self.__cursor.fetchone()

        self.__flush_results()

        return result

    # def findAll(self, query, data=None):
    #     self.__cursor.execute(...)

    def create(self, query, data) -> int:
        self.__cursor.execute(query, data)
        return self.__cursor.lastrowid

    def __flush_results(self):
        try:
            self.__cursor.fetchall()
        except Exception:
            pass
