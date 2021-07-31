# internal
from src.ui.components import BaseWidget, BaseDialog
# pyqt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QLabel, QPushButton)


class OrderWidget(BaseWidget):
    """Order Widget"""
    def __init__(self, order_id, firstname, lastname, date, total, status):
        self.order_id = order_id
        self.firstname = firstname
        self.lastname = lastname
        self.date = date
        self.total = total
        self.status = status
        super().__init__()

    def setupWidget(self):
        pass

    def setStyles(self):
        pass


class SaveAllReport(BaseDialog):
    """Save All Report"""
    def __init__(self, parent):
        super().__init__(parent)
        # orders
        self._orders = dict()

    def setupLayout(self):
        super().setupLayout()
        # set dialog title
        self.setWindowTitle('Save all orders')
        # set dialog minimum size
        self.setMinimumSize(700, 437)

    def setupDialog(self):
        # scrollable area
        self.scrollableArea = QScrollArea()
        self.scrollableArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollableArea.setWidgetResizable(True)
        self.dialogLayout.addWidget(self.scrollableArea)
        # widget
        self.widget = QWidget(objectName='MainWidget')
        self.scrollableArea.setWidget(self.widget)
        # orders layout
        self.ordersLayout = QVBoxLayout()
        self.widget.setLayout(self.ordersLayout)

    def setupControl(self):
        pass

    def setStyles(self):
        self.setStyleSheet("""
            QScrollArea{
                border: none;
            }
            #MainWidget{
                background-color: white;
            }
        """)

    def setOrders(self, orders):
        pass
