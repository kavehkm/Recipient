# standard
import random
from datetime import datetime


class Invoices(object):
    """Invoices View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.invoices
        self.table = self.tab.invoicesTable
        # connect signals
        self.ui.menu.btnInvoices.clicked.connect(self.tab_handler)
        self.tab.btnRefresh.clicked.connect(self.refresh)
        self.tab.btnSaveAll.clicked.connect(self.save_all)
        self.table.itemDoubleClicked.connect(self.order_details)

    def tab_handler(self):
        self.get()
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    def get(self):
        status = ['Complete', 'Proccess', 'On Hold']
        first_names = ['Kaveh', 'Amin', 'Ahmad', 'Darya']
        last_names = ['Mehrbanian', 'Akbarzadeh', 'Ghalamdast', 'Safayi']
        randint = random.randint(1, 100)
        orders = [
            [randint + i,
             '#{} {} {}'.format(randint + i, random.choice(first_names), random.choice(last_names)),
             datetime.now(),
             random.choice(status),
             random.randint(1000, 10000)]
            for i in range(10)
        ]
        self.table.setRecords(orders)

    def refresh(self):
        self.get()

    def order_details(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            record = self.table.getRecord(index)
            print(*record)

    def save_all(self):
        pass
