# internal
from .table import Table
from .base_dialog import BaseDialog
# pyqt
from PyQt5.QtCore import pyqtSignal, QObject


class TableListSignals(QObject):
    """Table List Signals"""
    select = pyqtSignal(list)


class TableList(BaseDialog):
    """Table List"""
    def __init__(self, parent, columns, sizes=None):
        self.columns = columns
        self.sizes = sizes
        self.signals = TableListSignals()
        super().__init__(parent)

    def setupDialog(self):
        self.table = Table(self.columns, self.sizes)
        self.dialogLayout.addWidget(self.table)

    def connectSignals(self):
        self.table.itemDoubleClicked.connect(self.selectHandler)

    def setList(self, items):
        self.table.setRecords(items)

    def selectHandler(self):
        item_index = self.table.getCurrentRecordIndex()
        if item_index is not None:
            item = self.table.getRecord(item_index)
            self.signals.select.emit(item)
