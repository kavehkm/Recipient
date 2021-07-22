# standard
import os
import unittest
# internal
from src import db
from src import settings as s
# pyodbc
import pyodbc


class TestDB(unittest.TestCase):
    """Test DB module"""
    def test_connection(self):
        conn = db.connection(**s.get('moein'))
        self.assertIsInstance(conn, db.Connection)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        cursor.close()
        conn.close()

    def test_invalid_connection(self):
        with self.assertRaises(Exception) as cm:
            invalid_db = {
                'server': '.\InvalidDB',
                'username': 'Unknown',
                'password': 'NotS3cret',
                'database': 'DoesNotExists'
            }
            conn = db.connection(**invalid_db)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            cursor.close()
            conn.close()
        self.assertIsInstance(cm.exception, pyodbc.Error)


if __name__ == '__main__':
    unittest.main()
