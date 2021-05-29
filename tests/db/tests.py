# standard
import unittest
# internal
from src import db, settings as s
# pyodbc
import pyodbc


class TestDB(unittest.TestCase):
    """Test DB module"""
    def test_connection(self):
        server = '.\Moein1'
        username = 'sa'
        password = 'arta1'
        database = 'Moein'
        conn = db.connection(server, username, password, database)
        self.assertIsInstance(conn, pyodbc.Connection)
        with conn.cursor() as c:
            c.execute("SELECT @@VERSION")
        conn.close()

    def test_invalid_connection(self):
        server = '.\Moein666'
        username = 'sa666'
        password = '***'
        database = 'Moein666'
        with self.assertRaises(Exception) as cm:
            conn = db.connection(server, username, password, database)
        self.assertIsInstance(cm.exception, pyodbc.Error)


if __name__ == '__main__':
    unittest.main()
