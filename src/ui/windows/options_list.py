# internal
from src.translation import _
from src.ui.components import TableList, AddSMButton, CancelSMButton
# pyqt
from PyQt5.QtWidgets import QCheckBox


class OptionsList(TableList):
    """Options List"""
    def __init__(self, *args, **kwargs):
        kwargs['checkable'] = True
        super().__init__(*args, **kwargs)

    def setupControl(self):
        self.checkAll = QCheckBox('Select all')
        self.btnAddAll = AddSMButton(_('Add'))
        self.btnCancel = CancelSMButton(_('Cancel'))
        self.controlLayout.addWidget(self.checkAll)
        self.controlLayout.addWidget(self.btnAddAll)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
        self.checkAll.stateChanged.connect(self.checkAllHandler)

    def checkAllHandler(self):
        state = True if self.checkAll.isChecked() else False
        self.table.checkAll(state)
