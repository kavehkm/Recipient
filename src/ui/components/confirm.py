# internal
from .message import Message
# pyqt
from PyQt5.QtWidgets import QPushButton


class Confirm(Message):
    """Confirm"""
    def setupControl(self):
        super().setupControl()
        self.btnCancel = QPushButton('Cencel')
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
