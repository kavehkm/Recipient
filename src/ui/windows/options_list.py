# internal
from src.ui.components import TableList, AddSMButton, CancelSMButton


class OptionsList(TableList):
    """Options List"""
    def setupControl(self):
        self.btnAddAll = AddSMButton('Add all')
        self.btnCancel = CancelSMButton('Cancel')
        self.controlLayout.addWidget(self.btnAddAll)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
