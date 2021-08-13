# pyqt
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QLineEdit, QDateTimeEdit, QComboBox, QSpinBox


############
# LineEdit #
############
class BaseEdit(QLineEdit):
    """Recipient Base Edit"""
    # sizes
    HEIGHT = 30

    def __init__(self, *args, **kwargs):
        # check for password echo mode
        self.password = kwargs.pop('password', False)
        super().__init__(*args, **kwargs)
        self.setupEdit()

    def setupEdit(self):
        # set password echo mode on demand
        if self.password:
            self.setEchoMode(QLineEdit.Password)
        # set style
        styleSheet = f"""
            height: {self.HEIGHT}px;
        """
        self.setStyleSheet(styleSheet)


class SMEdit(BaseEdit):
    """Recipient Small Edit"""
    HEIGHT = 20


class MDEdit(BaseEdit):
    """Recipient Medium Edit"""
    HEIGHT = 30


class LGEdit(BaseEdit):
    """Recipient Large Edit"""
    HEIGHT = 40


############
# ComboBox #
############
class BaseCombo(QComboBox):
    """Recipient Base Combo"""
    # sizes
    HEIGHT = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupCombo()

    def setupCombo(self):
        # set style
        styleSheet = f"""
            padding-left: 10px;
            height: {self.HEIGHT}px;
        """
        self.setStyleSheet(styleSheet)


class SMCombo(BaseCombo):
    """Recipient Small Combo"""
    HEIGHT = 20


class MDCombo(BaseCombo):
    """Recipient Medium Combo"""
    HEIGHT = 30


class LGCombo(BaseCombo):
    """Recipient Large Combo"""
    HEIGHT = 40


################
# DateTimeEdit #
################
class BaseDataTimeEdit(QDateTimeEdit):
    """Recipeint Base DateTime Edit"""
    # sizes
    HEIGHT = 30
    # formatting
    DATETIME_FORMAT = 'yyyy-MM-ddTHH:mm:ss'
    DATETIME_DISPLAY_FORMAT = 'yyyy-MM-dd @ HH:mm:ss'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupDateTimeEdit()

    def setupDateTimeEdit(self):
        # set popup
        self.setCalendarPopup(True)
        # set display format
        self.setDisplayFormat(self.DATETIME_DISPLAY_FORMAT)
        # set style
        styleSheet = f"""
            height: {self.HEIGHT}px;
        """
        self.setStyleSheet(styleSheet)

    def setDateTime(self, datetimeString):
        super().setDateTime(QDateTime.fromString(datetimeString, self.DATETIME_FORMAT))

    def getDateTime(self):
        return self.dateTime().toString(self.DATETIME_FORMAT)


class SMDateTimeEdit(BaseDataTimeEdit):
    """Recipient Small DateTime Edit"""
    HEIGHT = 20


############
# Spin Box #
############
class BaseSpin(QSpinBox):
    """Recipient Base Spin"""
    # sizes
    HEIGHT = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupSpin()

    def setupSpin(self):
        # set style
        styleSheet = f"""
            height: {self.HEIGHT}px;
        """
        self.setStyleSheet(styleSheet)


class SMSpin(BaseSpin):
    """Recipient Small Spin"""
    HEIGHT = 20
