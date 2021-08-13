# pyqt
from PyQt5.QtWidgets import QTabWidget


class Tab(QTabWidget):
    """Recipient Tab"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupTab()

    def setupTab(self):
        self.setStyleSheet("""
            QTabBar::tab{
                width: 40ex;
                height: 15ex;
            }
        """)
