import time
import mysql.connector
from mysql.connector.cursor import MySQLCursor


class Cache:
    def __init__(self, cursor: MySQLCursor):
        self.cursor = cursor

    def get(self, name: str, ref:str):
        lower = time.time() - (24 * 3600)
        self.cursor.execute("SELECT * FROM general_cache WHERE name = %s AND ref = %s AND time >= %s ", (name, ref, lower))
        row = self.cursor.fetchone()
        if row is not None:
            return row[3]
        return None

    def set(self, name:str, ref:str, content:str):
        self.cursor.execute("INSERT INTO `general_cache`(`id`, `name`, `ref`, `content`, `time`) VALUES (NULL, %s, %s, %s, %s)",
                            (name, ref, content, time.time()))
        pass
