# internal
from src.ui.components import BaseDialog, Table
# pyqt
from PyQt5.QtWidgets import QPushButton


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
        # orders table
        self.ordersTable = Table(['ID', 'Order', 'Date', 'Status', 'Total'])
        self.dialogLayout.addWidget(self.ordersTable)

    def setupControl(self):
        # save button
        self.btnConfirm = QPushButton('Confirm')
        self.controlLayout.addWidget(self.btnConfirm)
        # cancel button
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnCancel)

    def setStyles(self):
        self.setStyleSheet("""
            QPushButton{
                min-height: 25px;
            }
        """)

    def connectSignals(self):
        self.btnCancel.clicked.connect(self.close)

    def setOrders(self, orders):
        # remove old orders
        self._orders = dict()
        self.ordersTable.removeAllRecords()
        # set new orders
        for index, order in enumerate(orders):
            firstname = order['billing']['first_name'] or order['shipping']['first_name']
            lastname = order['billing']['last_name'] or order['shipping']['last_name']
            key = '#{} {} {}'.format(order['id'], firstname, lastname)
            record = [
                order['id'],
                key,
                order['created_date'].strftime('%Y-%m-%d @ %H:%M'),
                order['status'],
                order['total']
            ]
            self.ordersTable.addRecord(record, index)
            self._orders[order['number']] = index
