# internal
from .message import Message
from src.translation import _
from .buttons import CancelSMButton


class Confirm(Message):
    """Confirm"""
    def setupControl(self):
        super().setupControl()
        self.btnCancel = CancelSMButton(_('Cencel'))
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
