# standard
import string
import random
import unittest
# internal
from src import settings
from src.wc import api
from src.wc import errors
from src.wc.base_model import WCBaseModel
# woocommerce
from woocommerce import API


INVALID_CREDENTIALS = {
    'url': settings.get('wc')['url'],
    'ckey': 'ck_nul1sbjblc9oc4lt8izq26hkwcib9vhxtx88an6e',
    'skey': 'cs_hwf9fvtntbu5ek105oez1obg99v5zijb6q5kcfqd',
    'version': 'wc/v3'
}


def slugify(name):
    lower_name = name.lower()
    return lower_name.replace(' ', '-')


class StatusCodes(object):
    """Status Codes Collection"""
    Success =       200     # success
    Created =       201     # created
    BadRequest =    400     # invalid request, e.g. using unsupported HTTP method
    Unauthorized =  401     # authentication or permission error, e.g. incorrect API keys
    NotFound =      404     # request to resources that dont exist or are missing
    InternalError = 500     # server error


class TestAPI(unittest.TestCase):
    """Test API module"""
    STATUS_CODES = StatusCodes()

    def test_connection(self):
        wcapi = api.get(**settings.get('wc'))
        response = wcapi.get("")
        self.assertEqual(response.status_code, self.STATUS_CODES.Success)

    def test_invalid_connection(self):
        wcapi = api.get(**INVALID_CREDENTIALS)
        response = wcapi.get("")
        self.assertEqual(response.status_code, self.STATUS_CODES.Unauthorized)


class TestWCBaseModel(unittest.TestCase):
    """Test WooCommerce Base Model"""
    STATUS_CODES = StatusCodes()

    @classmethod
    def setUpClass(cls):
        wc_settings = settings.get('wc')
        cls.wcapi = API(
            wc_settings.get('url'),
            wc_settings.get('ckey'),
            wc_settings.get('skey'),
            wp_api=True,
            version='wc/v3'
        )

    def setUp(self):
        # minimal product model
        self.endpoint = 'products'
        self.product_model = WCBaseModel()
        self.product_model.ENDPOINT = self.endpoint
        self.products_data = [
            {'name': 'product 1', 'slug': 'product-1', 'regular_price': '1000'},
            {'name': 'product 2', 'slug': 'product-2', 'regular_price': '2000'},
            {'name': 'product 3', 'slug': 'product-3', 'regular_price': '3000'}
        ]
        self.product_ids = []
        for data in self.products_data:
            product = self.wcapi.post(self.endpoint, data).json()
            self.product_ids.append(product['id'])

    def tearDown(self):
        for pid in self.product_ids:
            self.wcapi.delete('{}/{}'.format(self.endpoint, pid), params={'force': True})

    def test_endpoit(self):
        wcid = 100
        result = self.product_model._endpoint(wcid)
        expected = self.endpoint + '/' + str(wcid)
        self.assertEqual(result, expected)

    def test_unauthorized_request(self):
        wcapi = api.get(**INVALID_CREDENTIALS)
        product_model = WCBaseModel(wcapi)
        with self.assertRaises(Exception) as cm:
            product_model.all()
        self.assertIsInstance(cm.exception, errors.UnauthorizedError)

    def test_get(self):
        for pid in self.product_ids:
            result = self.product_model.get(pid)
            self.assertEqual(result.status_code, self.STATUS_CODES.Success)

    def test_get_with_invalid_id(self):
        with self.assertRaises(Exception) as cm:
            self.product_model.get(666)
        self.assertIsInstance(cm.exception, errors.NotFoundError)

    def test_all(self):
        result = self.product_model.all()
        self.assertEqual(result.status_code, self.STATUS_CODES.Success)
        self.assertEqual(len(result.json()), len(self.product_ids))

    def test_create(self):
        name = 'New Unittest Product {}'.format(''.join(random.choices(string.ascii_letters, k=5)))
        data = {
            'name': name,
            'regular_price': str(random.randint(1000, 10000)),
            'slug': slugify(name)
        }
        result = self.product_model.create(data)
        self.assertEqual(result.status_code, self.STATUS_CODES.Created)
        # check store
        wcid = result.json()['id']
        self.product_ids.append(wcid)
        result = self.product_model.get(wcid)
        self.assertEqual(result.status_code, self.STATUS_CODES.Success)
        self.assertEqual(result.json()['name'], data['name'])

    def test_update(self):
        regular_price = str(random.randint(1000, 10000))
        wcid = random.choice(self.product_ids)
        data = {
            'regular_price': regular_price
        }
        result = self.product_model.update(wcid, data)
        self.assertEqual(result.status_code, self.STATUS_CODES.Success)
        # check store
        result = self.product_model.get(wcid)
        self.assertEqual(result.status_code, self.STATUS_CODES.Success)
        self.assertEqual(result.json()['regular_price'], regular_price)

    def test_delete(self):
        wcid = random.choice(self.product_ids)
        result = self.product_model.delete(wcid)
        self.assertEqual(result.status_code, self.STATUS_CODES.Success)
        self.product_ids.remove(wcid)
        result = self.product_model.all(status='publish')
        self.assertEqual(len(result.json()), len(self.product_ids))


if __name__ == '__main__':
    unittest.main()
