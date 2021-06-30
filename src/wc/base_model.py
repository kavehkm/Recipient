# internal
from src.wc import api


class WCBaseModel(object):
    """WooCommerce Base Model"""
    ENDPOINT = 'wcbasemodel'

    def __init__(self, wcapi=None):
        if wcapi is None:
            wcapi = api.get()
        self.wcapi = wcapi

    def _endpoint(self, wcid):
        return '{}/{}'.format(self.ENDPOINT, wcid)

    def _request(self, method, endpoint, data, params=None):
        parameters = {
            'endpoint': endpoint,
            'params': params if params else {}
        }
        if data:
            parameters['data'] = data
        try:
            return getattr(self.wcapi, method)(**parameters)
        except Exception as e:
            raise e

    def get(self, wcid):
        return self._request('get', self._endpoint(wcid), None)

    def all(self, **params):
        return self._request('get', self.ENDPOINT, None, params)

    def create(self, data):
        return self._request('post', self.ENDPOINT, data)

    def update(self, wcid, data):
        return self._request('put', self._endpoint(wcid), data)

    def delete(self, wcid, **params):
        return self._request('delete', self._endpoint(wcid), None, params)
