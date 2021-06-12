# internal
from .base_dialog import BaseDialog
from src.ui.resources import icons
# pyqt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class Message(BaseDialog):
    """Message"""
    # levels
    SUCCESS =   0
    INFO =      1
    WARNING =   2
    ERROR =     3
    DEFAULT_LEVEL = INFO
    # level related titles
    TITLES = {
        SUCCESS:    'success',
        INFO:       'information',
        WARNING:    'warning',
        ERROR:      'error'
    }
    # level related icons
    ICONS = {
        SUCCESS:    ':/icons/successDialog.png',
        INFO:       ':/icons/infoDialog.png',
        WARNING:    ':/icons/warningDialog.png',
        ERROR:      ':/icons/errorDialog.png'
    }

    def __init__(self, parent, level, message, details=None):
        self.level = level
        self.message = message
        self.details = details
        super().__init__(parent)

    def setupDialog(self):
        super().setupDialog()
        # set proper title
        self.setWindowTitle(self.TITLES.get(self.level, self.DEFAULT_LEVEL))
        # contents layout
        contentsLayout = QHBoxLayout()
        self.dialogLayout.addLayout(contentsLayout)
        # - icon
        iconLayout = QVBoxLayout()
        icon = QLabel()
        pix = self.ICONS.get(self.level, self.DEFAULT_LEVEL)
        icon.setPixmap(QPixmap(pix))
        iconLayout.addWidget(icon)
        iconLayout.addStretch(1)
        contentsLayout.addLayout(iconLayout)
        # - message and details
        messageLayout = QVBoxLayout()
        self.lblMessage = QLabel(self.message)
        self.lblMessage.setObjectName('Message')
        messageLayout.addWidget(self.lblMessage)
        if self.details:
            self.lblDetails = QLabel(self.details)
            self.lblDetails.setObjectName('Details')
            messageLayout.addWidget(self.lblDetails)
        contentsLayout.addLayout(messageLayout)
        contentsLayout.addStretch(1)

    def setupControl(self):
        self.btnOk = QPushButton('OK')
        self.controlLayout.addWidget(self.btnOk)

    def setStyles(self):
        self.setStyleSheet("""
            #Message{
                font-size: 11px;
                padding: 10px;
            }
            #Details{
                color: grey;
                font-style: italic;
                padding: 10px;
            }
        """)

    def connectSignals(self):
        self.btnOk.clicked.connect(self.close)
