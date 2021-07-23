# standard
import unittest
# internal
from src import db
from src import settings as s
from src.models import Column, Model
from src.models.errors import DoesNotExistsError


class Order(Model):
    """Order Model"""
    __table_name__ = 'Orders'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    fname = Column(str)
    lname = Column(str)
    address = Column(str)


class Item(Model):
    """Item Model"""
    __table_name__ = 'Items'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    name = Column(str)
    price = Column(float)


class OrderItem(Model):
    """Order-Item Model"""
    __table_name__ = 'OrderItem'
    __primary_key__ = 'oid'
    # columns
    oid = Column(int)
    iid = Column(int)
    quantity = Column(int)


class TestModel(unittest.TestCase):
    """Test Model Class"""
    def setUp(self):
        # create database connection
        self.connection = db.connection(**s.get('testdb'))
        # create instances from models
        self.order = Order()
        self.item = Item()
        self.order_item = OrderItem()
        # set db connection for models
        self.order.connection = self.item.connection = self.order_item.connection = self.connection
        # create models tables
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
        cursor = self.connection.cursor()
        for table in tables:
            cursor.execute(table)
        cursor.close()
        self.connection.commit()
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
        inserts = {
            "INSERT INTO Items(id, name, price) VALUES (?, ?, ?)":                  self.items,
            "INSERT INTO Orders(id, fname, lname, address) VALUES (?, ?, ?, ?)":    self.orders,
            "INSERT INTO OrderItem(oid, iid, quantity) VALUES (?, ?, ?)":           self.order_items
        }
        cursor = self.connection.cursor()
        for sql, records in inserts.items():
            cursor.executemany(sql, records)
        cursor.close()
        self.connection.commit()

    def test__select_empty(self):
        expected_result = 'SELECT *'
        result = self.item._select()
        self.assertEqual(result, expected_result)

    def test__select_signle_table(self):
        cols = ['col1', 'col2', 'col3']
        expected_result = 'SELECT ' + ', '.join(cols)
        result = self.item._select(columns1=cols)
        self.assertEqual(result, expected_result)

    def test__select_joined_table(self):
        alias1 = 'X'
        cols1 = ['cola', 'colb', 'colc']
        alias2 = 'Y'
        cols2 = ['cold', 'cole', 'colf', 'colg']
        expected_result = 'SELECT X.cola, X.colb, X.colc, ' \
                          'Y.cold, Y.cole, Y.colf, Y.colg'
        result = self.item._select(alias1, cols1, alias2, cols2)
        self.assertEqual(result, expected_result)

    def test__where(self):
        kwargs = {
            'id': 1,
            'name': 'a',
            'price': 1000
        }
        expected_result = (' WHERE id = ? AND name = ? AND price = ?', [1, 'a', 1000])
        result = self.order._where(kwargs)
        self.assertTupleEqual(result, expected_result)

    def test_get_max_pk(self):
        result = self.item.get_max_pk()
        expected_result = self.items[-1][0]
        self.assertEqual(result, expected_result)

    def test_get_max_pk_against_commit(self):
        next_id = self.item.get_max_pk() + 1
        fields = {
            'id': next_id,
            'name': 'next item',
            'price': 1000
        }
        self.item.create(fields)
        result = self.item.get_max_pk()
        self.assertEqual(result, next_id)
        self.item.connection.commit()
        result = self.item.get_max_pk()
        self.assertEqual(result, next_id)

    def test_all(self):
        results = self.item.all()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), len(self.items))

    def test_filter(self):
        results = self.item.filter()
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), len(self.items))

    def test_filter_with_kwargs(self):
        kwargs = {
            'oid': 1
        }
        results = self.order_item.filter(**kwargs)
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 3)

    def test_get(self):
        expected_list = self.items[1]
        result = self.item.get(id=2)
        result_list = [result.id, result.name, result.price]
        self.assertListEqual(result_list, expected_list)

    def test_get_conditions(self):
        expected_list = self.items[2]
        result = self.item.get(name='item3')
        result_list = [result.id, result.name, result.price]
        self.assertListEqual(result_list, expected_list)

    def test_get_DoesNotExists(self):
        with self.assertRaises(Exception) as cm:
            self.item.get(id=666)
        self.assertIsInstance(cm.exception, DoesNotExistsError)

    def test_create(self):
        fields = {
            'id': len(self.items) + 1,
            'name': 'new product',
            'price': 1000
        }
        self.item.create(fields)
        self.item.connection.commit()
        results = self.item.all()
        self.assertEqual(len(results), len(self.items) + 1)

    def test_update(self):
        fields = {
            'name': 'edited product'
        }
        kwargs = {
            'id': 1
        }
        self.item.update(fields, **kwargs)
        self.item.connection.commit()
        result = self.item.get(1, 'name')
        self.assertEqual(result.name, fields['name'])

    def test_delete_all(self):
        self.order.delete()
        self.order.connection.commit()
        results = self.order.all()
        self.assertEqual(len(results), 0)

    def test_delete_with_kwargs(self):
        kwargs = {
            'id': 1
        }
        self.item.delete(**kwargs)
        self.item.connection.commit()
        results = self.item.all()
        self.assertEqual(len(results), len(self.items) - 1)

    def test_inner_join(self):
        results = self.order.inner_join(self.order_item, 'id', 'oid', ['id', 'fname', 'lname', 'address'], ['iid'])
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), len(self.order_items))

    def test_left_outer_join(self):
        results = self.item.left_outer_join(self.order_item, 'id', 'iid', ['id', 'name', 'price'])
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 2)

    def test_right_outer_join(self):
        results = self.order_item.right_outer_join(self.item, 'iid', 'id', ['id', 'name'])
        # check results data type
        self.assertIsInstance(results, list)
        # check count
        self.assertEqual(len(results), 2)

    def tearDown(self):
        # delete person table
        sql = "DROP TABLE {}"
        tables = ['Items', 'Orders', 'OrderItem']
        cursor = self.connection.cursor()
        for table in tables:
            cursor.execute(sql.format(table))
        cursor.close()
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
