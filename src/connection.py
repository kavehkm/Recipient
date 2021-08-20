# internal
from src import settings as s
# pyodbc
import pyodbc


class Connection(object):
    """Database Connection"""
    def __init__(self, server, username, password, database, autocommit):
        self._server = server
        self._username = username
        self._password = password
        self._database = database
        self._autocommit = autocommit
        # pyodbc connection
        self._connection = None

    @staticmethod
    def _driver():
        return [d for d in pyodbc.drivers() if d.find('SQL') != -1][0]

    def _dsn(self):
        dsn = 'driver={};server={};database={};uid={};pwd={}'
        return dsn.format(self._driver(), self._server, self._database, self._username, self._password)

    def _get_connection(self):
        if self._connection is None:
            self._connection = pyodbc.connect(self._dsn(), autocommit=self._autocommit)
        return self._connection

    def _safe_method(self, method, *args, **kwargs):
        if self._connection:
            return getattr(self._connection, method)(*args, **kwargs)

    def cursor(self):
        return self._get_connection().cursor()

    def commit(self):
        self._safe_method('commit')

    def rollback(self):
        self._safe_method('rollback')

    def close(self):
        self._safe_method('close')


def get(server=None, username=None, password=None, database=None, autocommit=False):
    db_settings = s.get('moein')
    server = server or db_settings['server']
    username = username or db_settings['username']
    password = password or db_settings['password']
    database = database or db_settings['database']
    return Connection(server, username, password, database, autocommit)
