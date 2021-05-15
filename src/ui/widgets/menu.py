# internal
from src.ui.resources import icons
# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class MenuWidget(QWidget):
    """Menu Widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupMenu()

    def setupMenu(self):
        # set general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        #
        # set buttons
        #
        # status
        self.btnStatus = QPushButton('Status')
        self.btnStatus.setIcon(QIcon(':/icons/btnStatus.png'))
        self.btnStatus.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnStatus)
        # invoices
        self.btnInvoices = QPushButton('Invoices')
        self.btnInvoices.setIcon(QIcon(':/icons/btnInvoices.png'))
        self.btnInvoices.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnInvoices)
        # update wp
        self.btnUpdateWP = QPushButton('Update WP')
        self.btnUpdateWP.setIcon(QIcon(':/icons/btnUpdateWP.png'))
        self.btnUpdateWP.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnUpdateWP)
        # settings
        self.btnSettings = QPushButton('Settings')
        self.btnSettings.setIcon(QIcon(':/icons/btnSettings.png'))
        self.btnSettings.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnSettings)
        # logs
        self.btnLogs = QPushButton('Logs')
        self.btnLogs.setIcon(QIcon(':/icons/btnLogs.png'))
        self.btnLogs.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnLogs)
        # help
        self.btnHelp = QPushButton('Help')
        self.btnHelp.setIcon(QIcon(':/icons/btnHelp.png'))
        self.btnHelp.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnHelp)
        # about
        self.btnAbout = QPushButton('About')
        self.btnAbout.setIcon(QIcon(':/icons/btnAbout.png'))
        self.btnAbout.setIconSize(QSize(24, 24))
        self.generalLayout.addWidget(self.btnAbout)
        # add stretch at the end
        self.generalLayout.addStretch(1)

        #
        # set style sheet
        #
        self.setStyleSheet("""
            QPushButton {
                height: 50px;
                text-align: left;
                padding-left: 20px
            }
        """)
