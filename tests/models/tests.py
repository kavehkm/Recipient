# standard
import unittest
from datetime import datetime
# internal
from src import connection
from src import settings as s
from src.models import Map, DoesNotExists


class TestModel(unittest.TestCase):
    """Test Model"""
    def setUp(self):
        self.conn = connection.get(**s.get('test_db'))
        self.test_map = Map('TestMap', 'test')
        self.test_map.set_connection(self.conn)
        # create TestMap models
        sql = """
            CREATE TABLE TestMap(
                id                      INT             PRIMARY KEY,
                wcid                    INT             NOT NULL        UNIQUE,
                last_update             DATETIME        NOT NULL,
                update_required         BIT             NOT NULL        DEFAULT 0
            )
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        # insert records into TestMap models
        sql = """
            INSERT INTO TestMap(id, wcid, last_update)
            VALUES (?, ?, ?)
        """
        self.records = [
            [i, i * 100, datetime.now()]
            for i in range(1, 11)
        ]
        cursor.executemany(sql, self.records)
        cursor.close()
        self.conn.commit()

    def tearDown(self):
        # delete TestMap models
        sql = "DROP TABLE TestMap"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        self.conn.close()

    def test_max(self):
        expected = self.records[-1][0]
        result = self.test_map.max('TestMap', 'id')
        self.assertEqual(expected, result)
        # part 2
        expected2 = self.records[-1][1]
        result2 = self.test_map.max('TestMap', 'wcid')
        self.assertEqual(expected2, result2)

    def test_max_against_commit(self):
        self.test_map.create(666, 666 * 1000, datetime.now())
        result = self.test_map.max('TestMap', 'id')
        self.assertEqual(666, result)
        # part 2
        result2 = self.test_map.max('TestMap', 'wcid')
        self.assertEqual(666 * 1000, result2)

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
        result = self.test_map.where(conditions)
        self.assertTupleEqual(expected, result)

    def test_get(self):
        expected = self.records[5][:2]
        obj = self.test_map.get(id=6)
        result = [obj.id, obj.wcid]
        self.assertListEqual(expected, result)

    def test_get_with_conditions(self):
        conditions = {
            'id': 10,
            'wcid': 10 * 100
        }
        expected = self.records[9][:2]
        obj = self.test_map.get(**conditions)
        result = [obj.id, obj.wcid]
        self.assertListEqual(expected, result)

    def test_get_does_not_exists(self):
        with self.assertRaises(Exception) as cm:
            self.test_map.get(id=666)
        self.assertIsInstance(cm.exception, DoesNotExists)

    def test_all(self):
        result = self.test_map.all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(self.records), len(result))

    def test_create(self):
        now = datetime.now()
        self.test_map.create(1000, 1000*1000, now)
        self.conn.commit()
        result = self.test_map.all()
        self.assertEqual(len(self.records)+1, len(result))
        # part 2
        obj = self.test_map.get(id=1000, wcid=1000*1000)
        result2 = [obj.id, obj.wcid]
        expected = [1000, 1000*1000]
        self.assertListEqual(expected, result2)

    def test_update(self):
        fields = {
            'id': 666,
            'wcid': 666 * 1000,
            'update_required': True
        }
        self.test_map.update(fields, id=5)
        self.conn.commit()
        obj = self.test_map.get(**fields)
        result = [obj.id, obj.wcid, obj.update_required]
        expected = [fields['id'], fields['wcid'], fields['update_required']]
        self.assertListEqual(expected, result)

    def test_delete_all(self):
        self.test_map.delete()
        self.conn.commit()
        result = self.test_map.all()
        self.assertEqual(0, len(result))

    def test_delete_with_conditions(self):
        self.test_map.delete(id=1)
        self.conn.commit()
        result = self.test_map.all()
        self.assertEqual(len(self.records) - 1, len(result))


if __name__ == '__main__':
    unittest.main()
