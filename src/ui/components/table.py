# pyqt
from PyQt5 import Qt
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem


class Table(QTableWidget):
    """Base Table"""
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.bootstrap()

    def bootstrap(self):
        self.setupTable()
        self.setStyles()

    def setupTable(self):
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.Qt.NoFocus)

    def setStyles(self):
        self.setStyleSheet("""
            QTableWidget{
                margin: 5px;
                selection-color: black;
                selection-background-color: #BCDCF4;
            }
        """)

    def getCurrentRecordIndex(self):
        currentRecordIndex = self.currentRow()
        return currentRecordIndex if currentRecordIndex > -1 else None

    def getRecord(self, recordIndex):
        record = []
        for colIndex in range(len(self.columns)):
            item = self.item(recordIndex, colIndex)
            record.append(item.text())
        return record

    def _fillRow(self, rowIndex, items):
        for colIndex, item in enumerate(items, 0):
            self.setItem(rowIndex, colIndex, QTableWidgetItem(str(item)))

    def addRecord(self, record):
        self.insertRow(0)
        self._fillRow(0, record)

    def updateRecord(self, recordIndex, newItems):
        self._fillRow(recordIndex, newItems)

    def removeRecord(self, recordIndex):
        self.removeRow(recordIndex)

    def removeAllRecords(self):
        self.clearContents()
        self.setRowCount(0)

    def setRecords(self, records):
        self.removeAllRecords()
        for record in records:
            self.addRecord(record)
