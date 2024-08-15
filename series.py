import sqlite3

from strings import Strings


def make_value(name: str, v: str):
    return "(NULL, '" + str(name) + "', '" + str(v) + "', 'saved')"


class Series:
    def __init__(self, db: sqlite3.Cursor):
        self.db = db

    def get(self, name):
        self.db.execute("SELECT content FROM series WHERE name = %s LIMIT 1", (name,))
        rows = self.db.fetchone()
        if rows is not None:
            return rows[0]
        else:
            return None

    def set(self, name: str, values: list):
        query_values = []
        for v in values:
            query_values.append(make_value(name,v))
        self.db.execute("INSERT INTO series_data (id, name, value, status) VALUES "+Strings.implode(", ", query_values))