# internal
from src.ui.resources import icons
# pyqt
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout,
                             QLabel, QPushButton, QProgressBar)


class BaseDialog(QDialog):
    """Base Dialog"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setupDialog()
        self.setStyles()
        self.connectSignals()

    def setupDialog(self):
        # set window modality
        self.setWindowModality(Qt.ApplicationModal)
        # general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

    def setStyles(self):
        pass

    def connectSignals(self):
        pass

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
        self.generalLayout.addLayout(contentsLayout)
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
        # control layout
        self.controlLayout = QHBoxLayout()
        self.controlLayout.addStretch(1)
        self.generalLayout.addLayout(self.controlLayout)
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


class Confirm(Message):
    """Confirm"""
    def setupDialog(self):
        super().setupDialog()
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        super().connectSignals()
        self.btnCancel.clicked.connect(self.close)


class Progress(BaseDialog):
    """Progress Dialog"""
    def __init__(self, parent, title, minimum, maximum):
        self.title = title
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(parent)

    def setupDialog(self):
        super().setupDialog()
        # set title
        self.setWindowTitle(self.title)
        # set size
        self.setMinimumSize(300, 100)
        # title layout
        titleLayout = QHBoxLayout()
        self.generalLayout.addLayout(titleLayout)
        self.lblTitle = QLabel(self.title)
        titleLayout.addWidget(self.lblTitle, alignment=Qt.AlignHCenter)
        # progress layout
        progressLayout = QHBoxLayout()
        self.generalLayout.addLayout(progressLayout)
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(self.minimum)
        self.progressBar.setMaximum(self.maximum)
        progressLayout.addWidget(self.progressBar)

    def connectSignals(self):
        self.progressBar.valueChanged.connect(self.onFinished)

    def setValue(self, value):
        if self.isHidden():
            self.show()
        self.progressBar.setValue(value)

    def onFinished(self, value):
        if value == self.progressBar.maximum():
            self.close()
