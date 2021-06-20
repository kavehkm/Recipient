# standard
import os
import unittest
# internal
from src import db, settings as s
# pyodbc
import pyodbc


class TestDB(unittest.TestCase):
    """Test DB module"""
    def setUp(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.databases_file = 'databases.json'
        self.databases_file_path = os.path.join(self.dir, self.databases_file)
        self.sa = s.SettingsAPI(self.databases_file_path)

    def test_connection(self):
        conn = db.connection(**self.sa.get('valid'))
        self.assertIsInstance(conn, pyodbc.Connection)
        with conn.cursor() as c:
            c.execute("SELECT @@VERSION")
        conn.close()

    def test_invalid_connection(self):
        with self.assertRaises(Exception) as cm:
            conn = db.connection(**self.sa.get('invalid'))
        self.assertIsInstance(cm.exception, pyodbc.Error)


if __name__ == '__main__':
    unittest.main()
