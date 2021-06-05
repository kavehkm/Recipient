class Help(object):
    """Help View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.help
        # connect signals
        self.ui.menu.btnHelp.clicked.connect(self.tab_handler)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.HELP)
