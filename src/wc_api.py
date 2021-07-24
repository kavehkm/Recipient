# internal
from src import settings as s
# woocommerce
from woocommerce import API


def get(url=None, ckey=None, skey=None, version=None, wp_api=True):
    wc_settings = s.get('wc', {})
    url = url or wc_settings.get('url')
    ckey = ckey or wc_settings.get('ckey')
    skey = skey or wc_settings.get('skey')
    version = version or wc_settings.get('version')
    # create wc api instance
    return API(url, ckey, skey, wp_api=wp_api, version=version)
