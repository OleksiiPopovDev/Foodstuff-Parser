import sqlite3
import os
import mysql.connector


class Connector:
    _connect = None

    def __init__(self):
        if not isinstance(self._connect, sqlite3.Connection):
            self.create_connection_mysql()

    def create_connection_sqlite(self):
        self._connect = sqlite3.connect('database/%s.db' % os.getenv('DB_FILE_NAME'))

    def create_connection_mysql(self):
        self._connect = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASS'),
            database=os.getenv('DB_FILE_NAME')
        )

    def get_cursor(self):
        return self._connect.cursor()

    def commit(self):
        self._connect.commit()
