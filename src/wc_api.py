# internal
from src import settings as s
# woocommerce
from woocommerce import API


def get(url=None, ckey=None, skey=None, version=None, timeout=None, wp_api=True):
    wc_settings = s.get('wc')
    url = url or wc_settings['url']
    ckey = ckey or wc_settings['ckey']
    skey = skey or wc_settings['skey']
    version = version or wc_settings['version']
    timeout = timeout or wc_settings['timeout']
    # create wc api instance
    return API(url, ckey, skey, wp_api=wp_api, version=version, timeout=timeout)
