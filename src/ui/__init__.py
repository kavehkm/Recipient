# internal
from src.ui.resources import icons
# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class UI(QMainWindow):
    """User Interface"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # set windows title
        self.setWindowTitle('Recipient')
        # set windows icon
        self.setWindowIcon(QIcon(':/icons/windowIcon.png'))
        # set windows geometry
        self.setGeometry(100, 100, 809, 500)
        # set window min size
        self.setMinimumSize(809, 500)
        # bootstrap
        self.bootstrap()

    def bootstrap(self):
        # setup ui
        self.setupUI()
        # connect signals
        self.connectSignals()

    def setupUI(self):
        pass

    def connectSignals(self):
        pass
