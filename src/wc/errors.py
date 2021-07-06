class WCBaseError(Exception):
    """WooCommerce Base Error"""
    MESSAGE = 'WooCommerce base error'
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
    MESSAGE = 'Connections error'


class BadRequestError(WCBaseError):
    """WooCommerce 400 Bad Request Error"""
    MESSAGE = 'Invalid request'


class UnauthorizedError(WCBaseError):
    """WooCommerce 401 Unauthorized Error"""
    MESSAGE = 'Authentication error'


class InternalServerError(WCBaseError):
    """WooCommerce Internal Server Error"""
    MESSAGE = 'Server internal error'


class NotFoundError(WCBaseError):
    """WooCommerce 404 Not Found Error"""
    MESSAGE = 'Requests to resources that dont exist or are missing'
