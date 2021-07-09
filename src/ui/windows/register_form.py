# internal
from src.ui.components import BaseDialog
# pyqt
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton


class RegisterFormSignals(QObject):
    """Register Form Signals"""
    showOptions = pyqtSignal(int)


class RegisterForm(BaseDialog):
    """Register Form"""
    ID = 0
    WCID = 1

    def __init__(self, parent):
        self.signals = RegisterFormSignals()
        super().__init__(parent)

    def setupDialog(self):
        self.form = QFormLayout()
        self.dialogLayout.addLayout(self.form)
        # id
        self.id = QLineEdit()
        self.idOptions = QPushButton('...')
        self.idOptions.setObjectName('Options')
        idLayout = QHBoxLayout()
        idLayout.addWidget(self.id)
        idLayout.addWidget(self.idOptions)
        self.form.addRow(QLabel('ID'), idLayout)
        # wcid
        self.wcid = QLineEdit()
        self.wcidOptions = QPushButton('...')
        self.wcidOptions.setObjectName('Options')
        wcidLayout = QHBoxLayout()
        wcidLayout.addWidget(self.wcid)
        wcidLayout.addWidget(self.wcidOptions)
        self.form.addRow(QLabel('WCID'), wcidLayout)

    def setupControl(self):
        self.btnSave = QPushButton('Save')
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnSave)
        self.controlLayout.addWidget(self.btnCancel)

    def setStyles(self):
        self.setStyleSheet("""
            #Options{
                max-width: 25px;
            }
        """)

    def connectSignals(self):
        self.btnCancel.clicked.connect(self.close)
        self.idOptions.clicked.connect(lambda: self.signals.showOptions.emit(self.ID))
        self.wcidOptions.clicked.connect(lambda: self.signals.showOptions.emit(self.WCID))

    def getId(self):
        return self.id.text()

    def setId(self, value):
        self.id.setText(value)

    def getWcid(self):
        return self.wcid.text()

    def setWcid(self, value):
        self.wcid.setText(value)

    def clear(self):
        self.id.clear()
        self.wcid.clear()
