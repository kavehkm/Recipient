# standard
import unittest
import random
# internal
from src import wc
from src import wc_api
from src import settings as s


invalid_credentials = {
    'url': s.get('test_store')['url'],
    'ckey': 'ck_nul1sbjblc9oc4lt8izq26hkwcib9vhxtx88an6e',
    'skey': 'cs_hwf9fvtntbu5ek105oez1obg99v5zijb6q5kcfqd',
    'version': 'wc/v3'
}


class TestWC(unittest.TestCase):
    """Test WooCommerce"""
    def setUp(self):
        self.endpoint = 'products'
        api = wc_api.get(**s.get('test_store'))
        self.wc_product = wc.get(api, self.endpoint)
        self.product_ids = []
        self.products_data = [
            {'name': f'product {i}', 'regular_price': f'{i}000'}
            for i in range(1, 4)
        ]
        for data in self.products_data:
            product = self.wc_product.create(data)
            self.product_ids.append(product['id'])

    def tearDown(self):
        for pid in self.product_ids:
            self.wc_product.delete(pid)

    def test_endpoint(self):
        wcid = 100
        expected = '{}/{}'.format(self.endpoint, wcid)
        result = self.wc_product._endpoint(wcid)
        self.assertEqual(expected, result)

    def test_unauthorized_request(self):
        api = wc_api.get(**invalid_credentials)
        wc_product = wc.get(api, 'products')
        with self.assertRaises(Exception) as cm:
            wc_product.all()
        self.assertIsInstance(cm.exception, wc.UnauthorizedError)

    def test_get(self):
        for pid in self.product_ids:
            self.wc_product.get(pid)

    def test_get_with_invalid_id(self):
        with self.assertRaises(Exception) as cm:
            self.wc_product.get(666666)
        self.assertIsInstance(cm.exception, wc.NotFoundError)

    def test_all(self):
        for i in range(100, 121):
            product = self.wc_product.create({'name': f'product {i}'})
            self.product_ids.append(product['id'])
        result = self.wc_product.all()
        self.assertEqual(len(self.product_ids), len(result))

    def test_all_excludes(self):
        excludes = self.product_ids[:3]
        result = self.wc_product.all(excludes=excludes)
        self.assertEqual(len(self.product_ids) - len(excludes), len(result))

    def test_create(self):
        name = 'New Unittest Product'
        data = {
            'name': name,
            'regular_price': '1000000'
        }
        result = self.wc_product.create(data)
        wcid = result['id']
        self.product_ids.append(wcid)
        self.wc_product.get(wcid)
        self.assertEqual(name, result['name'])

    def test_update(self):
        regular_price = '2000000'
        wcid = random.choice(self.product_ids)
        data = {
            'regular_price': regular_price
        }
        self.wc_product.update(wcid, data)
        result = self.wc_product.get(wcid)
        self.assertEqual(regular_price, result['regular_price'])

    def test_delete(self):
        wcid = random.choice(self.product_ids)
        self.wc_product.delete(wcid)
        self.product_ids.remove(wcid)
        result = self.wc_product.all(status='publish')
        self.assertEqual(len(self.product_ids), len(result))


if __name__ == '__main__':
    unittest.main()
