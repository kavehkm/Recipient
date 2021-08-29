# pyqt
from PyQt5 import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem


class Table(QTableWidget):
    """Base Table"""
    def __init__(self, columns, sizes=None, parent=None):
        super().__init__(parent)
        self.columns = columns
        # if sizes not specify, set all column size equal
        if sizes is None:
            sizes = [1 for _ in columns]
        self.sizes = sizes
        # bootstrap table
        self.bootstrap()

    def bootstrap(self):
        self.setupTable()
        self.setStyles()

    def setupTable(self):
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.setLayoutDirection(Qt.Qt.RightToLeft)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        # stretch last section
        horizontalHeader = self.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._setColumnsSize()

    def _setColumnsSize(self):
        # compute base width
        base = self.horizontalHeader().width() // sum(self.sizes)
        # resize each column
        for i, size in enumerate(self.sizes):
            self.setColumnWidth(i, size * base)

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

    def addRecord(self, record, recordIndex=0):
        self.insertRow(recordIndex)
        self._fillRow(recordIndex, record)

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

    def findRecord(self, value):
        items = self.findItems(str(value), Qt.Qt.MatchExactly)
        return items[0].row() if items else None

    def highlightRecord(self, recordIndex, qColor):
        for colIndex in range(len(self.columns)):
            self.item(recordIndex, colIndex).setBackground(qColor)
