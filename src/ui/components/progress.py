# pyqt
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QProgressDialog


class Progress(QProgressDialog):
    """Progress"""
    def __init__(self, parent, title, minimum, maximum):
        super().__init__(title, '', minimum, maximum, parent)
        self.setWindowTitle(title)
        self.setCancelButton(None)
        self.setWindowModality(Qt.ApplicationModal)

    def setWindowTitle(self, a0: str) -> None:
        title = 'Recipient-{}'.format(a0)
        super().setWindowTitle(title)
