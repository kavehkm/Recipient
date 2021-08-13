# pyqt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget


class ScrollArea(QScrollArea):
    """Recipient Scroll Area"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupScroll()

    def setupScroll(self):
        # set policies
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        # set widget
        self.widget = QWidget()
        self.setWidget(self.widget)
        # set stylesheet
        self.setStyleSheet("""
            QScrollArea{
                border: none;
            }
        """)

    def setLayout(self, a0):
        self.widget.setLayout(a0)
