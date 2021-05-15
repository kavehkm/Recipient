# internal
from src.ui.resources import icons
from src.ui.widgets import MenuWidget, ContentsWidget
# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout


class UI(QMainWindow):
    """User Interface"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # set windows title
        self.setWindowTitle('Recipient')
        # set windows icon
        windowIcon = QIcon()
        windowIcon.addFile(':/icons/windowIcon16.png', QSize(16, 16))
        windowIcon.addFile(':/icons/windowIcon24.png', QSize(24, 24))
        windowIcon.addFile(':/icons/windowIcon32.png', QSize(32, 32))
        windowIcon.addFile(':/icons/windowIcon48.png', QSize(48, 48))
        windowIcon.addFile(':/icons/windowIcon96.png', QSize(96, 96))
        windowIcon.addFile(':/icons/windowIcon256.png', QSize(256, 256))
        self.setWindowIcon(windowIcon)
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
        # set central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # set general layout
        self.generalLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.generalLayout)
        # set menu widget 30%
        self.generalLayout.addWidget(MenuWidget(), 30)
        # set content widget 70%
        self.generalLayout.addWidget(ContentsWidget(), 70)

    def connectSignals(self):
        pass
