import sqlite3
import os


class Connector:
    _connect: sqlite3.Connection = None

    def __init__(self):
        if not isinstance(self._connect, sqlite3.Connection):
            self.create_connection()

    def create_connection(self):
        self._connect = sqlite3.connect('database/%s.db' % os.getenv('DB_FILE_NAME'))

    def get_cursor(self) -> sqlite3.Cursor:
        return self._connect.cursor()

    def commit(self):
        self._connect.commit()
