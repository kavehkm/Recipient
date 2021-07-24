# standard
import unittest
# internal
from src import settings as s
from src import connection
from src import table


class TestTable(unittest.TestCase):
    """Test Database Table"""
    def setUp(self):
        # create database connection
        self.conn = connection.get(**s.get('test_db'))
        # create tables
        tables = [
            """
            CREATE TABLE Items(
                id          INT             PRIMARY KEY,
                name        VARCHAR(255)    NOT NULL,
                price       FLOAT           NOT NULL          
            );
            """,
            """
            CREATE TABLE Orders(
                id          INT             PRIMARY KEY,
                fname       VARCHAR(255)    NOT NULL,
                lname       VARCHAR(255)    NOT NULL,
                address     VARCHAR(255)    NOT NULL
            );
            """,
            """
            CREATE TABLE OrderItem(
                oid         INT             NOT NULL,
                iid         INT             NOT NULL,
                quantity    INT             NOT NULL
            )
            """
        ]
        cursor = self.conn.cursor()
        for t in tables:
            cursor.execute(t)
        cursor.close()
        self.conn.commit()
        # insert some test records to tables
        self.items = [
            [1, 'item1', 100],
            [2, 'item2', 200],
            [3, 'item3', 300],
            [4, 'item4', 400],
            [5, 'item5', 500]
        ]
        self.orders = [
            [1, 'fname1', 'lname1', 'address1'],
            [2, 'fname2', 'lname2', 'address2'],
        ]
        self.order_items = [
            [1, 1, 2],
            [1, 2, 5],
            [1, 3, 3],
            [2, 1, 1],
            [2, 2, 5]
        ]
        cursor = self.conn.cursor()
        cursor.executemany(
            "INSERT INTO Items(id, name, price) VALUES (?, ?, ?)",
            self.items
        )
        cursor.executemany(
            "INSERT INTO Orders(id, fname, lname, address) VALUES (?, ?, ?, ?)",
            self.orders
        )
        cursor.executemany(
            "INSERT INTO OrderItem(oid, iid, quantity) VALUES (?, ?, ?)",
            self.order_items
        )
        cursor.close()
        self.conn.commit()

        # create table classes
        self.item_table = table.get('Items', 'id')
        self.item_table.set_connection(self.conn)
        self.order_table = table.get('Orders', 'id')
        self.order_table.set_connection(self.conn)
        self.order_item_table = table.get('OrderItem', 'oid')
        self.order_item_table.set_connection(self.conn)

    def tearDown(self):
        sql = "DROP TABLE {}"
        tables = ['Items', 'Orders', 'OrderItem']
        cursor = self.conn.cursor()
        for t in tables:
            cursor.execute(sql.format(t))
        cursor.close()
        self.conn.commit()
        self.conn.close()

    def test_select_all(self):
        expected = 'SELECT *'
        result = table.Table.select()
        self.assertEqual(expected, result)

    def test_select_single_table(self):
        cols = ['col1', 'col2', 'col3']
        expected = 'SELECT ' + ', '.join(cols)
        result = table.Table.select(columns1=cols)
        self.assertEqual(expected, result)

    def test_select_joined_table(self):
        alias1, alias2 = 'X', 'Y'
        cols1, cols2 = ['a', 'b', 'c'], ['r', 's', 't', 'u']
        expected = 'SELECT X.a, X.b, X.c, Y.r, Y.s, Y.t, Y.u'
        result = table.Table.select(alias1, cols1, alias2, cols2)
        self.assertEqual(expected, result)

    def test_where(self):
        kwargs = {
            'id': 1,
            'name': 'somename',
            'price': 1000
        }
        expected = (' WHERE id = ? AND name = ? AND price = ?', [1, 'somename', 1000])
        result = table.Table.where(kwargs)
        self.assertTupleEqual(expected, result)

    def test_max_pk(self):
        expected = self.items[-1][0]
        result = self.item_table.max_pk()
        self.assertEqual(expected, result)

    def test_max_pk_against_commit(self):
        next_id = self.item_table.max_pk() + 1
        fields = {
            'id': next_id,
            'name': 'next item',
            'price': 1000
        }
        self.item_table.create(fields)
        result = self.item_table.max_pk()
        self.assertEqual(next_id, result)
        self.conn.commit()
        result = self.item_table.max_pk()
        self.assertEqual(next_id, result)

    def test_all(self):
        result = self.item_table.all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(self.items), len(result))

    def test_filter(self):
        result = self.item_table.filter()
        self.assertIsInstance(result, list)
        self.assertEqual(len(self.items), len(result))

    def test_filter_with_conditions(self):
        kwargs = {
            'oid': 1
        }
        result = self.order_item_table.filter(**kwargs)
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))

    def test_get(self):
        expected = self.items[1]
        item = self.item_table.get(id=2)
        result = [item.id, item.name, item.price]
        self.assertListEqual(expected, result)

    def test_get_with_conditions(self):
        expected = self.items[2]
        item = self.item_table.get(name='item3')
        result = [item.id, item.name, item.price]
        self.assertListEqual(expected, result)

    def test_get_DoesNotExists(self):
        with self.assertRaises(Exception) as cm:
            self.item_table.get(id=6666)
        self.assertIsInstance(cm.exception, table.DoesNotExistsError)

    def test_create(self):
        fields = {
            'id': len(self.items) + 1,
            'name': 'new item',
            'price': 1000
        }
        self.item_table.create(fields)
        self.conn.commit()
        result = self.item_table.all()
        self.assertEqual(len(self.items) + 1, len(result))

    def test_update(self):
        fields = {
            'name': 'edited item'
        }
        kwargs = {
            'id': 1
        }
        self.item_table.update(fields, **kwargs)
        self.conn.commit()
        result = self.item_table.get(1, 'name')
        self.assertEqual(fields['name'], result.name)

    def test_delete_all(self):
        self.order_table.delete()
        self.conn.commit()
        result = self.order_table.all()
        self.assertEqual(0, len(result))

    def test_delete_with_conditions(self):
        kwargs = {
            'id': 1
        }
        self.item_table.delete(**kwargs)
        self.conn.commit()
        result = self.item_table.all()
        self.assertEqual(len(self.items) - 1, len(result))

    def test_inner_join(self):
        result = self.order_table.inner_join(
            self.order_item_table,
            'id',
            'oid',
            ['id', 'fname', 'lname', 'address'],
            ['iid']
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(self.order_items), len(result))

    def test_left_outer_join(self):
        result = self.item_table.left_outer_join(
            self.order_item_table,
            'id',
            'iid',
            ['id', 'name', 'price']
        )
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))

    def test_right_outer_join(self):
        result = self.order_item_table.right_outer_join(
            self.item_table,
            'iid',
            'id',
            ['id', 'name']
        )
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))


if __name__ == '__main__':
    unittest.main()
