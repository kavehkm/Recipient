# internal
from src import views


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
