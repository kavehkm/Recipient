# internal
from src.ui.components import TableList
# pyqt
from PyQt5.QtWidgets import QPushButton


class AddEditOptions(TableList):
    """Add/Edit Options"""
    def setupControl(self):
        self.btnAddAll = QPushButton('Add All')
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnAddAll)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
