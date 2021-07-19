# internal
from . import api, errors


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
            response = getattr(self.wcapi, method)(**parameters)
        except Exception:
            raise errors.ConnectionsError
        else:
            status_code = response.status_code
            response = response.json()
            if status_code == 200 or status_code == 201:
                return response
            elif status_code == 400:
                e = errors.BadRequestError
            elif status_code == 401:
                e = errors.UnauthorizedError
            elif status_code == 404:
                e = errors.NotFoundError
            elif status_code == 500:
                e = errors.InternalServerError
            else:
                e = errors.WCBaseError
            raise e(details=response.get('message'))

    def get(self, wcid):
        return self._request('get', self._endpoint(wcid), None)

    def all(self, **params):
        page = 1
        results = []
        params['per_page'] = 100
        excludes = params.pop('excludes', [])
        while True:
            params['page'] = page
            objects = self._request('get', self.ENDPOINT, None, params)
            if objects:
                results.extend(objects)
                page += 1
            else:
                break
        if excludes:
            results = list(filter(lambda obj: obj['id'] not in excludes, results))
        return results

    def create(self, data):
        return self._request('post', self.ENDPOINT, data)

    def update(self, wcid, data):
        return self._request('put', self._endpoint(wcid), data)

    def delete(self, wcid, **params):
        return self._request('delete', self._endpoint(wcid), None, params)
