class WCBaseError(Exception):
    """WooCommerce Base Error"""
    MESSAGE = 'WooCommerce Base Error'
    DETAILS = ''

    def __init__(self, *args, message='', details=''):
        super().__init__(*args)
        self.message = message or self.MESSAGE
        self.details = details or self.DETAILS

    def __str__(self):
        if self.details:
            return '{}: {}'.format(self.message, self.details)
        else:
            return self.message


class ConnectionsError(WCBaseError):
    """WooCommerce Connections Error"""
    MESSAGE = 'Connections Error'


class BadRequestError(WCBaseError):
    """WooCommerce 400 Bad Request Error"""
    MESSAGE = 'Invalid Request'


class UnauthorizedError(WCBaseError):
    """WooCommerce 401 Unauthorized Error"""
    MESSAGE = 'Authentication Error'


class InternalServerError(WCBaseError):
    """WooCommerce Internal Server Error"""
    MESSAGE = 'Server Internal Error'


class NotFoundError(WCBaseError):
    """WooCommerce 404 Not Found Error"""
    MESSAGE = 'Requests to resources that dont exist or are missing'
