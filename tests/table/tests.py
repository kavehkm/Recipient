# standard
import unittest
from datetime import datetime
# internal
from src import connection
from src import settings as s
from src.table import DoesNotExists, Table


class TestTable(unittest.TestCase):
    """Test Table"""
    def setUp(self):
        self.conn = connection.get(**s.get('test_db'))
        self.test_table = Table('Test')
        self.test_table.connection = self.conn
        # create test table
        sql = """
            CREATE TABLE Test(
                c1      INT             PRIMARY KEY,
                c2      VARCHAR(50)     NOT NULL,
                c3      DATETIME        NOT NULL,
                c4      BIT             NOT NULL
            )
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        # insert records into Test table
        sql = """
            INSERT INTO Test(c1, c2, c3, c4)
            VALUES (?, ?, ?, ?)
        """
        self.records = [
            [i, 'test{}'.format(i), datetime.now(), True]
            for i in range(1, 11)
        ]
        cursor.executemany(sql, self.records)
        cursor.close()
        self.conn.commit()

    def tearDown(self):
        # drop test table
        sql = "DROP TABLE Test"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        self.conn.close()

    def test_does_not_exists(self):
        name = 'TestObject'
        conditions = {'a': 1, 'b': 2, 'c': 3}
        dne = DoesNotExists(name, conditions)
        result = str(dne)
        expected = 'TestObject with a:1, b:2, c:3 does not exists.'
        self.assertEqual(expected, result)

    def test_select(self):
        # test1
        expected1 = 'SELECT *'
        result1 = self.test_table.select()
        self.assertEqual(expected1, result1)
        # test2
        expected2 = 'SELECT a, b, c, d'
        result2 = self.test_table.select('a', 'b', 'c', 'd')
        self.assertEqual(expected2, result2)

    def test_where(self):
        conditions = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4
        }
        expected = (
            ' WHERE a = ? AND b = ? AND c = ? AND d = ?',
            [1, 2, 3, 4]
        )
        result = self.test_table.where(conditions)
        self.assertTupleEqual(expected, result)

    def test_max(self):
        expected = self.records[-1][0]
        result = self.test_table.max('c1')
        self.assertEqual(expected, result)

    def test_max_against_commit(self):
        fields = {
            'c1': 6666,
            'c2': '6666',
            'c3': datetime.now(),
            'c4': True
        }
        self.test_table.create(fields)
        result = self.test_table.max('c1')
        self.assertEqual(fields['c1'], result)

    def test_get(self):
        expected = self.records[5][:2]
        obj = self.test_table.get(c1=6)
        result = [obj.c1, obj.c2]
        self.assertListEqual(expected, result)

    def test_get_with_conditions(self):
        conditions = {
            'c1': 1,
            'c2': 'test1'
        }
        expected = self.records[0][:2]
        obj = self.test_table.get(**conditions)
        result = [obj.c1, obj.c2]
        self.assertListEqual(expected, result)

    def test_get_does_not_exists(self):
        with self.assertRaises(Exception) as cm:
            self.test_table.get(c1=666)
        self.assertIsInstance(cm.exception, DoesNotExists)

    def test_all(self):
        result = self.test_table.all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(self.records), len(result))

    def test_create(self):
        fields = {
            'c1': 666,
            'c2': 'test666',
            'c3': datetime.now(),
            'c4': True
        }
        self.test_table.create(fields)
        self.conn.commit()
        result = self.test_table.all()
        self.assertEqual(len(self.records) + 1, len(result))
        # part2
        obj = self.test_table.get(c1=fields['c1'])
        result2 = [obj.c1, obj.c2]
        expected2 = [fields['c1'], fields['c2']]
        self.assertListEqual(expected2, result2)

    def test_update(self):
        fields = {
            'c1': 666,
            'c2': 'test666'
        }
        self.test_table.update(fields, c1=1)
        self.conn.commit()
        obj = self.test_table.get(**fields)
        result = [obj.c1, obj.c2]
        expected = [fields['c1'], fields['c2']]
        self.assertListEqual(expected, result)

    def test_delete_all(self):
        self.test_table.delete()
        self.conn.commit()
        result = self.test_table.all()
        self.assertEqual(0, len(result))

    def test_delete_with_conditions(self):
        self.test_table.delete(c1=10)
        self.conn.commit()
        result = self.test_table.all()
        self.assertEqual(len(self.records) - 1, len(result))

    def test_custome_sql(self):
        sql = """
            SELECT *
            FROM Test AS A
            INNER JOIN Test AS B ON A.c1 = B.c1
        """
        result = self.test_table.custom_sql(sql, method='fetchall')
        self.assertEqual(len(self.records), len(result))


if __name__ == '__main__':
    unittest.main()
