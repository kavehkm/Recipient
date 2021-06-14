# pyqt
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout


class BaseDialog(QDialog):
    """Base Dialog"""
    def __init__(self, parent):
        super().__init__(parent)
        self.bootstrap()

    def bootstrap(self):
        self.setupLayout()
        self.setupDialog()
        self.setupControl()
        self.setStyles()
        self.connectSignals()

    def setupLayout(self):
        # general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        # dialog layout
        self.dialogLayout = QVBoxLayout()
        self.generalLayout.addLayout(self.dialogLayout)
        # control layout
        self.controlLayout = QHBoxLayout()
        self.controlLayout.addStretch(1)
        self.generalLayout.addLayout(self.controlLayout)
        # set window modality
        self.setWindowModality(Qt.ApplicationModal)

    def setupDialog(self):
        pass

    def setupControl(self):
        pass

    def setStyles(self):
        pass

    def connectSignals(self):
        pass

    def setWindowTitle(self, a0: str) -> None:
        title = 'Recipient-{}'.format(a0)
        super().setWindowTitle(title)
