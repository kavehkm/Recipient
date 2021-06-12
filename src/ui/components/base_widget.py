# pyqt
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class BaseWidget(QWidget):
    """Base Widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # bootstrap
        self.bootstrap()

    def bootstrap(self):
        self.setupLayout()
        self.setupWidget()
        self.setStyles()
        self.connectSignals()

    def setupLayout(self):
        # general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

    def setupWidget(self):
        pass

    def setStyles(self):
        pass

    def connectSignals(self):
        pass
