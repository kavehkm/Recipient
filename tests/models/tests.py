# standard
import os
import unittest
# internal
from src import db, settings
from src.models import Column, Model
# pyodbc
import pyodbc


class PersonModel(Model):
    """Person Model"""
    # db table info
    __table_name__ = 'Person'
    __primary_key__ = 'id'
    # columns
    pid = Column('id', 'wpid')
    age = Column('age', 'wpage')
    last_name = Column('lname', 'wplname')
    first_name = Column('fname', 'wpfname')


class TestModel(unittest.TestCase):
    """Test Model Class"""

    def setUp(self):
        # create database connection
        self.connection = db.connection(**settings.get('moein'))
        # create instance from PersonModel
        self.model = PersonModel()
        # set instance connection
        self.model.connection = self.connection
        # set number of records in Person table
        self.records_count = 4
        # create Person table with sample records
        sql_table = """
            CREATE TABLE Person(
                id      INT PRIMARY  KEY IDENTITY ,
                fname   VARCHAR(255) NOT NULL,
                lname   VARCHAR(255) NOT NULL,
                age     INT NOT NULL,
            )
        """
        sql_insert = """
            INSERT INTO Person(fname, lname, age) VALUES
            ('a', 'aa', 1),
            ('b', 'bb', 2),
            ('c', 'cc', 3),
            ('d', 'dd', 4)
        """
        for sql in [sql_table, sql_insert]:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
        self.connection.commit()

    def test__select(self):
        result = self.model._select()
        expected_result = 'SELECT id AS pid, age AS age, ' \
                          'lname AS last_name, fname AS first_name'
        self.assertEqual(result, expected_result)

    def test__where(self):
        kwargs = {
            'age': 26,
            'first_name': 'a'
        }
        result = self.model._where(kwargs)
        expected_result = (' WHERE age = ? AND fname = ?', [26, 'a'])
        self.assertTupleEqual(result, expected_result)

    def test_all(self):
        results = self.model.all()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), self.records_count)

    def test_filter(self):
        results = self.model.filter()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), self.records_count)

    def test_filter_with_kwargs(self):
        kwargs = {
            'first_name': 'a',
            'last_name': 'aa'
        }
        results = self.model.filter(**kwargs)
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 1)
        # check data
        result = results[0]
        self.assertEqual(result.age, 1)

    def test_get(self):
        result = self.model.get(4)
        result_list = [result.pid, result.first_name, result.last_name]
        expected_list = [4, 'd', 'dd']
        self.assertListEqual(result_list, expected_list)

    def test_get_DoesNotExists(self):
        result = self.model.get(666)
        self.assertIsNone(result)

    def test_create(self):
        fields = {
            'first_name': 'e',
            'last_name': 'ee',
            'age': 5
        }
        self.model.create(fields)
        self.connection.commit()
        results = self.model.all()
        self.assertEqual(len(results), self.records_count + 1)

    def test_update(self):
        fields = {
            'first_name': 'x',
            'last_name': 'xx',
            'age': 666
        }
        kwargs = {
            'pid': 1
        }
        self.model.update(fields, **kwargs)
        self.connection.commit()
        result = self.model.get(1)
        result_list = [result.pid, result.first_name, result.last_name, result.age]
        expected_list = [1, fields['first_name'], fields['last_name'], fields['age']]
        self.assertListEqual(result_list, expected_list)

    def test_delete_all(self):
        self.model.delete()
        self.connection.commit()
        results = self.model.all()
        self.assertEqual(len(results), 0)

    def test_delete_with_kwargs(self):
        kwargs = {
            'first_name': 'a',
            'last_name': 'aa'
        }
        self.model.delete(**kwargs)
        self.connection.commit()
        results = self.model.all()
        self.assertEqual(len(results), 3)

    def tearDown(self):
        # delete person table
        sql = "DROP TABLE Person"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
