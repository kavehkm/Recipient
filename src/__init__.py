class Controller(object):
    """Controller"""
    def __init__(self, ui):
        self.ui = ui
        self.bootstrap()

    def bootstrap(self):
        self.connect_signals()

    def connect_signals(self):
        # menu buttons
        self.ui.menu.btnStatus.clicked.connect(self.status_handler)
        self.ui.menu.btnInvoices.clicked.connect(self.invoices_handler)
        self.ui.menu.btnUpdateWP.clicked.connect(self.updateWP_handler)
        self.ui.menu.btnSettings.clicked.connect(self.settings_handler)
        self.ui.menu.btnLogs.clicked.connect(self.logs_handler)
        self.ui.menu.btnHelp.clicked.connect(self.help_handler)
        self.ui.menu.btnAbout.clicked.connect(self.about_handler)

    def status_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def invoices_handler(self):
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    def updateWP_handler(self):
        self.ui.contents.showTab(self.ui.contents.UPDATE_WP)

    def settings_handler(self):
        self.ui.contents.showTab(self.ui.contents.SETTINGS)

    def logs_handler(self):
        self.ui.contents.showTab(self.ui.contents.LOGS)

    def help_handler(self):
        self.ui.contents.showTab(self.ui.contents.HELP)

    def about_handler(self):
        self.ui.contents.showTab(self.ui.contents.ABOUT)
