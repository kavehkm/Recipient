# standard
import unittest
# internal
from src import settings as s
from src import wc_api


invalid_credentials = {
    'url': s.get('test_store')['url'],
    'ckey': 'ck_nul1sbjblc9oc4lt8izq26hkwcib9vhxtx88an6e',
    'skey': 'cs_hwf9fvtntbu5ek105oez1obg99v5zijb6q5kcfqd',
    'version': 'wc/v3'
}


class StatusCode(object):
    """Status Codes Collection"""
    Success =       200     # success
    Created =       201     # created
    BadRequest =    400     # invalid request, e.g. using unsupported HTTP method
    Unauthorized =  401     # authentication or permission error, e.g. incorrect API keys
    NotFound =      404     # request to resources that dont exist or are missing
    InternalError = 500     # server error


class TestWCAPI(unittest.TestCase):
    """Test wc_api module"""
    STATUS_CODES = StatusCode()

    def test_get(self):
        api = wc_api.get()
        response = api.get("products")
        self.assertEqual(self.STATUS_CODES.Success, response.status_code)

    def test_get_with_invalid_credentials(self):
        api = wc_api.get(**invalid_credentials)
        response = api.get("products")
        self.assertEqual(self.STATUS_CODES.Unauthorized, response.status_code)


if __name__ == '__main__':
    unittest.main()
