# pyqt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class BaseTab(QWidget):
    """Base Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupTab()
        self.setStyles()

    def setupTab(self):
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        self.generalLayout.setContentsMargins(0, 0, 0, 0)

    def setStyles(self):
        pass


class StatusTab(BaseTab):
    """Status Tab"""
    def __init__(self):
        super().__init__()
        # default state: stopped
        self.stop()

    def setupTab(self):
        super().setupTab()
        # service frame
        self.serviceFrame = QFrame()
        self.serviceFrame.setObjectName('ServiceFrame')
        self.generalLayout.addWidget(self.serviceFrame)
        # service layout
        self.serviceLayout = QVBoxLayout()
        self.serviceFrame.setLayout(self.serviceLayout)
        # service name
        self.serviceName = QLabel('<h2>Recipient Engine</h2>')
        self.serviceName.setFixedHeight(60)
        self.serviceLayout.addWidget(self.serviceName)
        # service state
        serviceStateLayout = QHBoxLayout()
        serviceStateLayout.setContentsMargins(0, 10, 0, 10)
        self.serviceStateLabel = QLabel('<b>status: </b>')
        self.serviceStateVal = QLabel()
        serviceStateLayout.addWidget(self.serviceStateLabel)
        serviceStateLayout.addWidget(self.serviceStateVal)
        serviceStateLayout.addStretch(1)
        self.serviceLayout.addLayout(serviceStateLayout)
        # service control
        serviceControlLayout = QHBoxLayout()
        self.serviceStart = QPushButton('start')
        self.serviceStop = QPushButton('stop')
        serviceControlLayout.addWidget(self.serviceStart)
        serviceControlLayout.addWidget(self.serviceStop)
        serviceControlLayout.addStretch(1)
        self.serviceLayout.addLayout(serviceControlLayout)
        # add stretch at the end
        self.generalLayout.addStretch(1)

    def setStyles(self):
        self.setStyleSheet("""
            #ServiceFrame{
                border: 1px solid silver;
                border-right-width: 15px;
            }
            #ServiceFrame[state="start"]{
                border-right-color: #26d926;
            }
            #ServiceFrame[state="stop"]{
                border-right-color: red;
            }
            #ServiceFrame[state="connecting"]{
                border-right-color: orange;
            }
        """)

    def start(self):
        self.serviceStateVal.setText('running')
        self.serviceStart.setDisabled(True)
        self.serviceStop.setEnabled(True)
        self.serviceFrame.setProperty('state', 'start')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def stop(self):
        self.serviceStateVal.setText('stopped')
        self.serviceStart.setEnabled(True)
        self.serviceStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'stop')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def connecting(self):
        self.serviceStateVal.setText('connecting')
        self.serviceStart.setDisabled(True)
        self.serviceStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'connecting')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())


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
