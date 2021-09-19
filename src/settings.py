# standard
import os
import json
from datetime import datetime, timedelta


########################
# application settings #
########################
# base directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# settings file name
SETTINGS_FILE_NAME = 'settings.json'


# settings file path
SETTINGS_FILE_PATH = os.path.join(
    BASE_DIR, SETTINGS_FILE_NAME
)


# apllication info
APP_NAME = 'recipient'
APP_VERSION = 1.1
APP_AUTHOR = 'Kaveh Mehrbanian'
APP_CONTRIBUTORS = [
    'Amin Eidgahian'
]


# network check settings
IP = '8.8.8.8'
PORT = 53
TIMEOUT = 3
INTERVAL = 3
JITTER = 1


# localization settings
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')
LOCALE_DOMAIN = 'recipient'
LOCALE_LANGUAGES = {
    'English': 'en',
    'Persian': 'fa'
}
LOCALE_DEFAULT_LANG = LOCALE_LANGUAGES['English']


# general settings
GENERAL_LANGUAGE = 'English'


# woocommerce settings
WC_URL = ''
WC_CONSUMER_KEY = ''
WC_SECREY_KEY = ''
WC_API_VERSION = 'wc/v3'
WC_API_TIMEOUT = 10


# moein settings
MOEIN_DB_SERVER = ''
MOEIN_DB_USERNAME = ''
MOEIN_DB_PASSWORD = ''
MOEIN_DB_NAME = ''


# import/export settings
IMPORT_EXPORT_SKU_HINT = False


# orders settings
now = datetime.now()
after = now - timedelta(days=7)
before = now + timedelta(days=365*20)
ORDERS_AFTER = after.replace(microsecond=0).isoformat()
ORDERS_BEFORE = before.replace(microsecond=0).isoformat()
ORDERS_STATUS = ['processing', 'on-hold', 'completed']


# invoices settings
INVOICES_TYPE = 0
INVOICES_REPOSITORY = 1
INVOICES_PRICE_LEVEL = 1
INVOICES_BUY_PRICE_TYPE = 1
INVOICES_SELL_PRICE_TYPE = 2
INVOICES_GUEST_CUSTOMER_ID = 1


# engine settings
ENGINE_AUTO_START = False
ENGINE_WC_UPDATE = True
ENGINE_CONVERT_ORDERS = False
ENGINE_INTERVAL = 30


#####################################
# application customizable settings #
#####################################
CUSTOMIZABLE_SETTINGS = {
    'general': {
        'language': GENERAL_LANGUAGE
    },
    'wc': {
        'url': WC_URL,
        'ckey': WC_CONSUMER_KEY,
        'skey': WC_SECREY_KEY,
        'version': WC_API_VERSION,
        'timeout': WC_API_TIMEOUT
    },
    'moein': {
        'server': MOEIN_DB_SERVER,
        'username': MOEIN_DB_USERNAME,
        'password': MOEIN_DB_PASSWORD,
        'database': MOEIN_DB_NAME
    },
    'import_export': {
        'sku_hint': IMPORT_EXPORT_SKU_HINT
    },
    'orders': {
        'status': ORDERS_STATUS,
        'after': ORDERS_AFTER,
        'before': ORDERS_BEFORE
    },
    'invoices': {
        'type': INVOICES_TYPE,
        'repository': INVOICES_REPOSITORY,
        'price_level': INVOICES_PRICE_LEVEL,
        'guest': INVOICES_GUEST_CUSTOMER_ID
    },
    'engine': {
        'auto_start': ENGINE_AUTO_START,
        'wc_update': ENGINE_WC_UPDATE,
        'convert_orders': ENGINE_CONVERT_ORDERS,
        'interval': ENGINE_INTERVAL
    }
}


################
# settings api #
################

# settings api class
class SettingsAPI(object):
    """Settings API"""
    def __init__(self, settings_file):
        self._settings_file = settings_file
        try:
            f = open(self._settings_file, 'rt')
            self._contents = json.loads(f.read())
            f.close()
        except Exception:
            self._contents = CUSTOMIZABLE_SETTINGS

    @property
    def contents(self):
        return self._contents

    def get(self, key, default=None):
        return self._contents.get(key, default)

    def set(self, key, value):
        self._contents[key] = value

    def save(self):
        f = open(self._settings_file, 'wt')
        f.write(json.dumps(self._contents, indent=4))
        f.close()


#########################
# settings.py interface #
#########################

_sa = SettingsAPI(SETTINGS_FILE_PATH)

contents = _sa.contents

get = _sa.get

set = _sa.set

save = _sa.save
