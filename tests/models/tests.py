# standard
import unittest
# internal
from src.models import Product


class TestPorductModel(unittest.TestCase):
    """Test Product Models"""
    def test_getinfo(self):
        info = '\n'.join([
            'line info 1',
            'line info 2',
            '[]',
            '[key1]',
            '[key2  ]',
            '[!nvalid xxyyzz]',
            '[sku abcdefg1234567]',
            '[barcode !@#$%^&*()_]'
        ])
        expected = {
            'key2': '',
            'sku': 'abcdefg1234567',
            'barcode': '!@#$%^&*()_'
        }
        result = Product.getinfo(info)
        self.assertDictEqual(expected, result)

    def test_getinfo_with_empty(self):
        info = ''
        expected = dict()
        result = Product.getinfo(info)
        self.assertDictEqual(expected, result)

    def test_getinfo_with_None(self):
        info = None
        expected = dict()
        result = Product.getinfo(info)
        self.assertDictEqual(expected, result)

    def test_setinfo(self):
        info = '\n'.join([
            'line info 1',
            'line info 2',
            '[key1 value1]',
            '[key2 value2]',
            '[!invalidkey value3]'
        ])
        d = {
            'key1': 'new value1',
            'key2': 'new value2',
            'key3': 'new value3'
        }
        expected = '\n'.join([
            'line info 1',
            'line info 2',
            '[key1 new value1]',
            '[key2 new value2]',
            '[!invalidkey value3]',
            '[key3 new value3]'
        ])
        result = Product.setinfo(info, d)
        self.assertEqual(expected, result)

    def test_setinfo_with_empty(self):
        info = ''
        d = {
            'sku': 'abcdefg1234567',
            'color': 'red',
            'size': 'L'
        }
        expected = '\n'.join([
            '[sku abcdefg1234567]',
            '[color red]',
            '[size L]'
        ])
        result = Product.setinfo(info, d)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
