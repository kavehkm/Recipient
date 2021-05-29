# standard
import os
import json
import unittest
# internal
from src import settings as s


class TestSettings(unittest.TestCase):
    """Test Settings Module"""
    def setUp(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = 'test_settings.json'
        self.settings_file_path = os.path.join(self.dir, self.settings_file)
        self.settings_file_contents = {
            'set1': {
                'a': 1,
                'b': 2,
                'c': 3
            },
            'set2': {
                'k1': [1, 2, 3, 4],
                'k2': 'This Is Some String'
            },
            'key1': ['member1', 'member2', 'member3'],
            'key2': 19.9,
            'key3': 'key3value'
        }
        with open(self.settings_file_path, 'wt') as f:
            f.write(json.dumps(self.settings_file_contents, indent=4))

    def test_does_not_exist_file(self):
        file_path = os.path.join(self.dir, 'does_not_exists_settings.json')
        sa = s.SettingsAPI(file_path)
        expected1 = s.CUSTOMIZABLE_SETTINGS
        result1 = sa.contents
        self.assertEqual(expected1, result1)
        expected2 = s.CUSTOMIZABLE_SETTINGS['wc']
        result2 = sa.get('wc')
        self.assertEqual(expected2, result2)

    def test_exist_file(self):
        sa = s.SettingsAPI(self.settings_file_path)
        expected1 = self.settings_file_contents
        result1 = sa.contents
        self.assertEqual(expected1, result1)
        expected2 = self.settings_file_contents['key3']
        result2 = sa.get('key3')
        self.assertEqual(expected2, result2)

    def test_get(self):
        sa = s.SettingsAPI(self.settings_file_path)
        for key, value in self.settings_file_contents.items():
            expected = value
            result = sa.get(key)
            self.assertEqual(expected, result)

    def test_get_notfound(self):
        sa = s.SettingsAPI(self.settings_file_path)
        self.assertIsNone(sa.get('666'))

    def test_get_default(self):
        sa = s.SettingsAPI(self.settings_file_path)
        expected = 'default'
        result = sa.get('666', expected)
        self.assertEqual(expected, result)

    def test_set(self):
        sa = s.SettingsAPI(self.settings_file_path)
        key_value = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': 'v3'
        }
        for key, value in key_value.items():
            sa.set(key, value)
        for key, value in key_value.items():
            expected = value
            result = sa.get(key)
            self.assertEqual(expected, result)

    def test_save(self):
        file_path = os.path.join(self.dir, 'does_not_exists_settings.json')
        key_value = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': 'v3',
            'k4': ['v41', 'v42', 'v43', 'v44']
        }
        sa = s.SettingsAPI(file_path)
        for key, value in key_value.items():
            sa.set(key, value)
        sa.save()
        self.assertTrue(os.path.exists(file_path))
        expected = {**s.CUSTOMIZABLE_SETTINGS, **key_value}
        result = sa.contents
        self.assertEqual(expected, result)

    def tearDown(self):
        for file in os.listdir(self.dir):
            if file.endswith('.json'):
                os.remove(os.path.join(self.dir, file))


if __name__ == '__main__':
    unittest.main()
