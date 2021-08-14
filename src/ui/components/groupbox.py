# pyqt
from PyQt5.QtWidgets import QGroupBox


class GpBox(QGroupBox):
    """Recipient GroupBox"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupGroup()

    def setupGroup(self):
        # set font
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        # set style
        self.setStyleSheet("""
            QGroupBox{
                padding: 20px
            }
        """)