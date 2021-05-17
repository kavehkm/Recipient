# pyqt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class BaseTab(QWidget):
    """Base Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupTab()

    def setupTab(self):
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        self.generalLayout.setContentsMargins(0, 0, 0, 0)


class StatusTab(BaseTab):
    """Status Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Status Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class InvoicesTab(BaseTab):
    """Invoices Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Invoices Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class UpdateWPTab(BaseTab):
    """Update WP Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>UpdateWP Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class SettingsTab(BaseTab):
    """Settings Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Settings Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class LogsTab(BaseTab):
    """Logs Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Logs Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class HelpTab(BaseTab):
    """Help Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Help Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class AboutTab(BaseTab):
    """About Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>About Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class ContentsWidget(QWidget):
    """Contents Widget"""
    STATUS =    0
    INVOICES =  1
    UPDATE_WP = 2
    SETTINGS =  3
    LOGS =      4
    HELP =      5
    ABOUT =     6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.setupContents()

    def setupContents(self):
        # set general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        """
        attach tabs
        """
        # status
        self.status = StatusTab()
        # invoices
        self.invoices = InvoicesTab()
        # update_wp
        self.updateWP = UpdateWPTab()
        # settings
        self.settings = SettingsTab()
        # logs
        self.logs = LogsTab()
        # help
        self.help = HelpTab()
        # about
        self.about = AboutTab()
        """
        register tabs
        """
        self.tabs = [
            self.status,
            self.invoices,
            self.updateWP,
            self.settings,
            self.logs,
            self.help,
            self.about
        ]
        for tab in self.tabs:
            self.generalLayout.addWidget(tab)
        """
        set default tab
        """
        self.showTab(self.STATUS)

    def showTab(self, tabId):
        for tab in self.tabs:
            tab.hide()
        self.tabs[tabId].show()
