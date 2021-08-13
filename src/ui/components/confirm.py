# internal
from .message import Message
from .buttons import SMButton


class Confirm(Message):
    """Confirm"""
    def setupControl(self):
        super().setupControl()
        self.btnCancel = SMButton('Cencel')
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
