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
        # set windows geometry
        self.setGeometry(100, 100, 809, 500)
        # set window min size
        self.setMinimumSize(809, 500)
        # bootstrap
        self.bootstrap()

    def bootstrap(self):
        # setup window icon
        self.setupWindowIcon()
        # setup ui
        self.setupUI()
        # connect signals
        self.connectSignals()

    def setupWindowIcon(self):
        windowIcon = QIcon()
        sizes = [16, 24, 32, 48, 96, 256]
        for size in sizes:
            iconFile = ':/icons/windowIcon{}.png'.format(size)
            windowIcon.addFile(iconFile, QSize(size, size))
        self.setWindowIcon(windowIcon)

    def setupUI(self):
        # set central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # set general layout
        self.generalLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.generalLayout)
        # set menu widget 30%
        self.menu = MenuWidget()
        self.generalLayout.addWidget(self.menu, 30)
        # set content widget 70%
        self.contents = ContentsWidget()
        self.generalLayout.addWidget(self.contents, 70)

    def connectSignals(self):
        pass
