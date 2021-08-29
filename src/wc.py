# internal
from src.translation import _


class WCBaseError(Exception):
    """WooCommerce Base Error"""
    message = _('WooCommerce base error')

    def __init__(self, *args, details=''):
        super().__init__(*args)
        self.details = details

    def __str__(self):
        return '{}: {}'.format(self.message, self.details)


class ConnectionsError(WCBaseError):
    """WooCommerce Connections Error"""
    message = _('Connections error')


class BadRequestError(WCBaseError):
    """WooCommerce 400 Bad Request Error"""
    message = _('Invalid request')


class UnauthorizedError(WCBaseError):
    """WooCommerce 401 Unauthorized Error"""
    message = _('Authentication error')


class InternalServerError(WCBaseError):
    """WooCommerce Internal Server Error"""
    message = _('Server internal error')


class NotFoundError(WCBaseError):
    """WooCommerce 404 Not Found Error"""
    message = _('Requests to resources that dont exist or are missing')


class WC(object):
    """WooCommerce"""
    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

    def _endpoint(self, wcid):
        return '{}/{}'.format(self.endpoint, wcid)

    def _request(self, method, endpoint, data, params=None):
        parameters = {
            'endpoint': endpoint,
            'params': params if params else {}
        }
        if data:
            parameters['data'] = data
        try:
            response = getattr(self.api, method)(**parameters)
        except Exception:
            raise ConnectionsError()
        else:
            status_code = response.status_code
            response = response.json()
            if status_code == 200 or status_code == 201:
                return response
            elif status_code == 400:
                e = BadRequestError
            elif status_code == 401:
                e = UnauthorizedError
            elif status_code == 404:
                e = NotFoundError
            elif status_code == 500:
                e = InternalServerError
            else:
                e = WCBaseError
            raise e(details=response.get('message'))

    def get(self, wcid):
        return self._request('get', self._endpoint(wcid), None)

    def all(self, **params):
        results = []
        # paging
        page = 1
        per_page = 100
        params['per_page'] = per_page
        while True:
            params['page'] = page
            objects = self._request('get', self.endpoint, None, params)
            results.extend(objects)
            if not objects or len(objects) < per_page:
                break
            page += 1
        return results

    def create(self, data):
        return self._request('post', self.endpoint, data)

    def update(self, wcid, data):
        return self._request('put', self._endpoint(wcid), data)

    def delete(self, wcid, **params):
        return self._request('delete', self._endpoint(wcid), None, params)


def get(api, endpoint):
    return WC(api, endpoint)
