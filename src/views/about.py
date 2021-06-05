class About(object):
    """About View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.about
        # connect signals
        self.ui.menu.btnAbout.clicked.connect(self.tab_handler)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.ABOUT)
