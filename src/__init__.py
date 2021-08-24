# internal
from src import views
from src import settings as s


class Controller(object):
    """Controller"""
    def __init__(self, ui):
        self.ui = ui
        # views
        self.status = views.Status(self.ui)
        self.invoices = views.Invoices(self.ui)
        self.woocommerce = views.WooCommerce(self.ui)
        self.settings = views.Settings(self.ui)
        self.logs = views.Logs(self.ui)
        self.help = views.Help(self.ui)
        self.about = views.About(self.ui)
        # bootstrap
        self._bootstrap()

    def _bootstrap(self):
        # check for engine auto start
        if s.get('engine')['auto_start']:
            self.status.start()
