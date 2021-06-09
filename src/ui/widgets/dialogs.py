# internal
from src.ui.resources import icons
# pyqt
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton


class BaseDialog(QDialog):
    """Base Dialog"""
    def __init__(self, parent):
        super().__init__(parent)
        # set window modality
        self.setWindowModality(Qt.ApplicationModal)

    def setWindowTitle(self, a0: str) -> None:
        title = 'Recipient-{}'.format(a0)
        super().setWindowTitle(title)


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
        super().__init__(parent)
        self.level = level
        self.message = message
        self.details = details
        # set proper title
        self.setWindowTitle(self.TITLES.get(self.level, self.DEFAULT_LEVEL))
        # setup dialog contents
        self.setupDialog()
        # setup dialog control
        self.setupControl()
        # set style sheet
        self.setStyles()
        # connect signals
        self.connectSignals()

    def setupDialog(self):
        # general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        # contents layout
        contentsLayout = QHBoxLayout()
        self.generalLayout.addLayout(contentsLayout)
        # _ icon
        iconLayout = QVBoxLayout()
        icon = QLabel()
        pix = self.ICONS.get(self.level, self.DEFAULT_LEVEL)
        icon.setPixmap(QPixmap(pix))
        iconLayout.addWidget(icon)
        iconLayout.addStretch(1)
        contentsLayout.addLayout(iconLayout)
        # _ message and details
        messageLayout = QVBoxLayout()
        self.lblMessage = QLabel(self.message)
        self.lblMessage.setObjectName('Message')
        messageLayout.addWidget(self.lblMessage)
        if self.details:
            self.lblDetails = QLabel(self.details)
            self.lblDetails.setObjectName('Details')
            messageLayout.addWidget(self.lblDetails)
        contentsLayout.addLayout(messageLayout)

    def setupControl(self):
        self.controlLayout = QHBoxLayout()
        self.generalLayout.addLayout(self.controlLayout)
        self.btnOk = QPushButton('Ok')
        self.controlLayout.addWidget(self.btnOk)
        self.controlLayout.setAlignment(self.btnOk, Qt.AlignHCenter)

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


class Confirm(Message):
    """Confirm"""
    def setupControl(self):
        super().setupControl()
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnCancel)
        self.controlLayout.setAlignment(self.btnCancel, Qt.AlignHCenter)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)
