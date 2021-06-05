class Status(object):
    """Status View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.status
        # connect signals
        self.ui.menu.btnStatus.clicked.connect(self.tab_handler)
        self.tab.btnStart.clicked.connect(self.start)
        self.tab.btnStop.clicked.connect(self.stop)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def start(self):
        self.tab.start()

    def stop(self):
        self.tab.stop()
