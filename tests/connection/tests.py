# standard
import unittest
# internal
from src import connection
# pyodbc
import pyodbc


# invalid credentials
invalid_credentials = {
    'server': '.\InvalidServer',
    'username': 'Unknown',
    'password': 'NotS3cret',
    'database': 'DoesNotExists'
}


class TestConnection(unittest.TestCase):
    """Test Database Connection"""
    def test_get(self):
        conn = connection.get()
        self.assertIsInstance(conn, connection.Connection)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        cursor.close()
        conn.close()

    def test_get_with_invalid_credentials(self):
        with self.assertRaises(Exception) as cm:
            conn = connection.get(**invalid_credentials)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            cursor.close()
            conn.close()
        self.assertIsInstance(cm.exception, pyodbc.Error)

    def test_safe_method(self):
        with self.assertRaises(Exception) as cm:
            conn = connection.get(**invalid_credentials)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
        # call rollback, commit and close on None must be safe
        conn.rollback()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()
