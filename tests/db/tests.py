# standard
import os
import unittest
# internal
from src import db, settings
# pyodbc
import pyodbc


class TestDB(unittest.TestCase):
    """Test DB module"""
    def test_connection(self):
        conn = db.connection(**settings.get('moein'))
        self.assertIsInstance(conn, pyodbc.Connection)
        with conn.cursor() as c:
            c.execute("SELECT @@VERSION")
        conn.close()

    def test_invalid_connection(self):
        with self.assertRaises(Exception) as cm:
            invalid_db = {
                'server': '.\InvalidDB',
                'username': 'Unknown',
                'password': 'NotS3cret',
                'database': 'DoesNotExists'
            }
            db.connection(**invalid_db)
        self.assertIsInstance(cm.exception, pyodbc.Error)


if __name__ == '__main__':
    unittest.main()
