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
        self.buttons = []
        self.setupMenu()
        self.setStyles()

    def setupMenu(self):
        # set general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        """
        set buttons
        """
        # status
        self.btnStatus = QPushButton('Status')
        self.btnStatus.setIcon(QIcon(':/icons/btnStatus.png'))
        # invoices
        self.btnInvoices = QPushButton('Invoices')
        self.btnInvoices.setIcon(QIcon(':/icons/btnInvoices.png'))
        # update wp
        self.btnUpdateWP = QPushButton('Update WP')
        self.btnUpdateWP.setIcon(QIcon(':/icons/btnUpdateWP.png'))
        # settings
        self.btnSettings = QPushButton('Settings')
        self.btnSettings.setIcon(QIcon(':/icons/btnSettings.png'))
        # logs
        self.btnLogs = QPushButton('Logs')
        self.btnLogs.setIcon(QIcon(':/icons/btnLogs.png'))
        # help
        self.btnHelp = QPushButton('Help')
        self.btnHelp.setIcon(QIcon(':/icons/btnHelp.png'))
        # about
        self.btnAbout = QPushButton('About')
        self.btnAbout.setIcon(QIcon(':/icons/btnAbout.png'))
        """
        register buttons
        """
        self.buttons = [
            self.btnStatus,
            self.btnInvoices,
            self.btnUpdateWP,
            self.btnSettings,
            self.btnLogs,
            self.btnHelp,
            self.btnAbout
        ]
        for btn in self.buttons:
            btn.setIconSize(QSize(24, 24))
            self.generalLayout.addWidget(btn)
        """
        add stretch at the end
        """
        self.generalLayout.addStretch(1)

    def setStyles(self):
        self.setStyleSheet("""
            QPushButton {
                height: 50px;
                text-align: left;
                padding-left: 20px
            }
        """)
