# standard
import unittest
# internal
from src.wc import api
from src import settings


class StatusCodes(object):
    """Status Codes Collection"""
    Success =       200     # success
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
        invalid_api = {
            'url': settings.get('wc')['url'],
            'ckey': 'ck_nul1sbjblc9oc4lt8izq26hkwcib9vhxtx88an6e',
            'skey': 'cs_hwf9fvtntbu5ek105oez1obg99v5zijb6q5kcfqd',
            'version': 'wc/v3'
        }
        wcapi = api.get(**invalid_api)
        response = wcapi.get("")
        self.assertEqual(response.status_code, self.STATUS_CODES.Unauthorized)
