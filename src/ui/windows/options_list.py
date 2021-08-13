# internal
from src.ui.components import TableList, SMButton


class OptionsList(TableList):
    """Options List"""
    def setupControl(self):
        self.btnAddAll = SMButton('Add all')
        self.btnCancel = SMButton('Cancel')
        self.controlLayout.addWidget(self.btnAddAll)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
