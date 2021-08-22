# internal
from .message import Message
from .buttons import CancelSMButton


class Confirm(Message):
    """Confirm"""
    def setupControl(self):
        super().setupControl()
        self.btnCancel = CancelSMButton('Cencel')
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
