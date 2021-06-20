# standard
import os
import unittest
# internal
from src import db, settings as s
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
    active = Column('active', 'wpactive')
    last_name = Column('lname', 'wplname')
    first_name = Column('fname', 'wpfname')


class TestModel(unittest.TestCase):
    """Test Model Class"""
    def setUp(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.database_file = 'database.json'
        self.database_file_path = os.path.join(self.dir, self.database_file)
        self.sa = s.SettingsAPI(self.database_file_path)
        self.connection = db.connection(**self.sa.get('db'))
        # create person table
        sql_table = """
            CREATE TABLE Person(
                id      INT PRIMARY  KEY IDENTITY ,
                fname   VARCHAR(255) NOT NULL,
                lname   VARCHAR(255) NOT NULL,
                age     INT NOT NULL,
                active  BIT NOT NULL DEFAULT 1
            )
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql_table)
        self.connection.commit()
        # insert some test records
        sql_insert = "INSERT INTO PERSON(fname, lname, age, active) VALUES (?, ?, ?, ?)"
        self.persons = [
            {
                'age': 11,
                'active': True,
                'first_name': 'a',
                'last_name': 'aa'
            },
            {
                'age': 12,
                'active': False,
                'first_name': 'b',
                'last_name': 'bb',
            },
            {
                'age': 13,
                'active': True,
                'first_name': 'c',
                'last_name': 'cc'
            }
        ]
        persons = [
            [person['first_name'], person['last_name'], person['age'], person['active']]
            for person in self.persons
        ]
        with self.connection.cursor() as cursor:
            cursor.executemany(sql_insert, persons)
        self.connection.commit()
        # create instance from PersonModel
        self.model = PersonModel()
        self.model.connection = self.connection

    def test_all(self):
        results = self.model.all()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), len(self.persons))
        # check data
        result = results[0]
        self.assertEqual(result.first_name, self.persons[0]['first_name'])

    def test_filter(self):
        results = self.model.filter()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), len(self.persons))
        # check data
        result = results[-1]
        self.assertEqual(result.active, self.persons[-1]['active'])

    def test_filter_with_kwargs1(self):
        kwargs = {
            'active': True
        }
        results = self.model.filter(**kwargs)
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 2)
        # check data
        result = results[0]
        self.assertEqual(result.age, self.persons[0]['age'])

    def test_filter_with_kwargs2(self):
        kwargs = {**self.persons[0]}
        results = self.model.filter(**kwargs)
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 1)
        # check data
        result = results[0]
        self.assertEqual(result.first_name, self.persons[0]['first_name'])

    def test_get(self):
        result = self.model.get(1)
        result_list = [result.pid, result.first_name, result.last_name, result.age, result.active]
        p1 = self.persons[0]
        excepted_list = [1, p1['first_name'], p1['last_name'], p1['age'], p1['active']]
        self.assertListEqual(result_list, excepted_list)

    def tearDown(self):
        # delete person table
        sql = "DROP TABLE Person"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
