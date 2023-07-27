import sqlite3


class Connector:
    _connect: sqlite3.Connection = None

    def __init__(self):
        if not isinstance(self._connect, sqlite3.Connection):
            self._connect = sqlite3.connect('test.db')

    def get_cursor(self) -> sqlite3.Cursor:
        return self._connect.cursor()

    def commit(self):
        self._connect.commit()
