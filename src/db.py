# internal
from src import settings as s
# pyodbc
import pyodbc


def connection(server=None, username=None, password=None, database=None, autocommit=False):
    db_settings = s.get('moein', {})
    server = server or db_settings.get('server')
    username = username or db_settings.get('username')
    password = password or db_settings.get('password')
    database = database or db_settings.get('database')
    driver = [d for d in pyodbc.drivers() if d.find('SQL') != -1][0]
    dsn = f'driver={driver};server={server};database={database};uid={username};pwd={password}'
    return pyodbc.connect(dsn, autocommit=autocommit)
