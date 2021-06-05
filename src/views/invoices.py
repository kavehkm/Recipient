class Invoices(object):
    """Invoices View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.invoices
        # connect signals
        self.ui.menu.btnInvoices.clicked.connect(self.tab_handler)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.INVOICES)
