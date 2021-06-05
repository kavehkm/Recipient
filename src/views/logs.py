class Logs(object):
    """Logs View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.logs
        # connect signals
        self.ui.menu.btnLogs.clicked.connect(self.tab_handler)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.LOGS)
