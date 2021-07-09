# internal
from src.ui.components import TableList
# pyqt
from PyQt5.QtWidgets import QPushButton


class OptionsList(TableList):
    """Options List"""
    def setupControl(self):
        self.btnAddAll = QPushButton('Add all')
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnAddAll)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
