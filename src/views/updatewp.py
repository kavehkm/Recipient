# standard
import time
import random
from datetime import datetime
# internal
from src.worker import Worker
from src.ui.widgets import Message, Confirm
# pyqt
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QProgressDialog


class ProductView(object):
    """Product View"""
    def __init__(self, parent):
        self.parent = parent
        self.tab = parent.tab
        self.table = parent.tab.productsTable

    def get(self):
        products = []
        for i in range(50):
            random_int = random.randint(1, 10000)
            product = [
                random_int,
                random_int + 1,
                f'Product{random_int}',
                random_int * 2,
                datetime.now().strftime('%Y/%m/%d')
            ]
            products.append(product)
        self.table.setRecords(products)

    def add(self):
        random_int = random.randint(1, 10000)
        new_product = [
            random_int,
            random_int + 1,
            f'Product{random_int}',
            random_int * 2,
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.table.addRecord(new_product)
        msg = Message(self.tab, Message.SUCCESS, 'New Product Added Successfully.')
        msg.show()

    def edit(self):
        product_index = self.table.getCurrentRecordIndex()
        if product_index is not None:
            product = self.table.getRecord(product_index)
            product[2] = product[2] + '-edited'
            self.table.updateRecord(product_index, product)
            msg = Message(self.tab, Message.SUCCESS, 'Product Edited Successfully.')
            msg.show()

    def remove(self):
        product_index = self.table.getCurrentRecordIndex()
        if product_index is not None:
            cfm = Confirm(self.tab, Confirm.WARNING, 'Are You Sure?')
            cfm.btnOk.clicked.connect(lambda: self.confirm_remove(product_index))
            cfm.show()

    def confirm_remove(self, product_index):
        self.table.removeRecord(product_index)
        msg = Message(self.tab, Message.SUCCESS, 'Product Removed Successfully.')
        msg.show()

    def update(self):
        # query database
        products = [i for i in range(50)]
        # progress dialog
        pd = QProgressDialog('Update Products...', 'Abort', 0, len(products), self.tab)
        # worker
        worker = Worker(self.updater, products)
        worker.signals.progress.connect(pd.setValue)
        worker.signals.error.connect(pd.close)
        worker.signals.error.connect(self.update_error)
        worker.signals.done.connect(self.update_done)
        # move worker to global threadpool and start progress
        QThreadPool.globalInstance().start(worker)
        # lock btnUpdateWP
        self.tab.btnUpdateWP.setDisabled(True)

    @staticmethod
    def updater(products, progress_callback):
        for i, products in enumerate(products, 1):
            time.sleep(0.5)
            progress_callback.emit(i)

    def update_error(self, e):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.tab, Message.ERROR, 'Cannot Update Products.', str(e))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.tab, Message.SUCCESS, 'Products Updated Successfully.')
        msg.show()


class CategoryView(object):
    """Category View"""
    def __init__(self, parent):
        self.parent = parent
        self.tab = parent.tab
        self.table = parent.tab.categoriesTable

    def get(self):
        categories = []
        for i in range(10):
            random_int = random.randint(1, 10000)
            category = [
                random_int,
                f'Category{random_int}',
                random_int * 2,
                datetime.now().strftime('%Y/%m/%d')
            ]
            categories.append(category)
        self.table.setRecords(categories)

    def add(self):
        random_int = random.randint(1, 10000)
        new_category = [
            random_int,
            f'Category{random_int}',
            random_int * 2,
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.table.addRecord(new_category)
        msg = Message(self.tab, Message.SUCCESS, 'New Category Added Successfully.')
        msg.show()

    def edit(self):
        category_index = self.table.getCurrentRecordIndex()
        if category_index is not None:
            category = self.table.getRecord(category_index)
            category[1] = category[1] + '-edited'
            self.table.updateRecord(category_index, category)
            msg = Message(self.tab, Message.SUCCESS, 'Category Edited Successfully.')
            msg.show()

    def remove(self):
        category_index = self.table.getCurrentRecordIndex()
        if category_index is not None:
            cfm = Confirm(self.tab, Confirm.WARNING, 'Are You Sure?')
            cfm.btnOk.clicked.connect(lambda: self.confirm_remove(category_index))
            cfm.show()

    def confirm_remove(self, category_index):
        self.table.removeRecord(category_index)
        msg = Message(self.tab, Message.SUCCESS, 'Category Removed Successfully.')
        msg.show()

    def update(self):
        # query database
        categories = [i for i in range(10)]
        # progress dialog
        pd = QProgressDialog('Update Categories...', 'Abort', 0, len(categories), self.tab)
        # worker
        worker = Worker(self.updater, categories)
        worker.signals.progress.connect(pd.setValue)
        worker.signals.error.connect(pd.close)
        worker.signals.error.connect(self.update_error)
        worker.signals.done.connect(self.update_done)
        # move worker to global threadpool and start progress
        QThreadPool.globalInstance().start(worker)
        # lock btnUpdateWP
        self.tab.btnUpdateWP.setDisabled(True)

    @staticmethod
    def updater(categories, progress_callback):
        for i, category in enumerate(categories, 1):
            time.sleep(0.5)
            progress_callback.emit(i)

    def update_error(self, e):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.tab, Message.ERROR, 'Cannot Update Categories.', str(e))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.tab, Message.SUCCESS, 'Categories Updated Successfully.')
        msg.show()


class UpdateWP(object):
    """UpdateWP View"""
    # tabs
    PRODUCTS = 0
    CATEGORIES = 10
    # action
    INIT = 1
    ADD = 2
    EDIT = 3
    REMOVE = 4
    UPDATE = 5
    # combination
    PRODUCTS_INIT = PRODUCTS + INIT
    PRODUCTS_ADD = PRODUCTS + ADD
    PRODUCTS_EDIT = PRODUCTS + EDIT
    PRODUCTS_REMOVE = PRODUCTS + REMOVE
    PRODUCTS_UPDATE = PRODUCTS + UPDATE
    CATEG0RIES_INIT = CATEGORIES + INIT
    CATEGORIES_ADD = CATEGORIES + ADD
    CATEGORIES_EDIT = CATEGORIES + EDIT
    CATEGORIES_REMOVE = CATEGORIES + REMOVE
    CATEGORIES_UPDATE = CATEGORIES + UPDATE

    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.updateWP
        # attach views
        self.product = ProductView(self)
        self.category = CategoryView(self)
        # connect signals
        self.ui.menu.btnUpdateWP.clicked.connect(self.tab_handler)
        self.tab.tabs.currentChanged.connect(lambda: self.dispatcher(self.INIT))
        self.tab.btnAdd.clicked.connect(lambda: self.dispatcher(self.ADD))
        self.tab.btnEdit.clicked.connect(lambda: self.dispatcher(self.EDIT))
        self.tab.btnRemove.clicked.connect(lambda: self.dispatcher(self.REMOVE))
        self.tab.btnUpdateWP.clicked.connect(lambda: self.dispatcher(self.UPDATE))

    def tab_handler(self):
        self.dispatcher(self.INIT)
        self.ui.contents.showTab(self.ui.contents.UPDATE_WP)

    def dispatcher(self, action):
        # find current tab const
        index = self.tab.tabs.currentIndex()
        if index == self.tab.PRODUCTS:
            current_tab = self.PRODUCTS
        else:
            current_tab = self.CATEGORIES
        # produce operation from current tab and action
        operation = current_tab + action
        # dispatch signal to proper view
        if operation == self.PRODUCTS_INIT:
            self.product.get()
        elif operation == self.PRODUCTS_ADD:
            self.product.add()
        elif operation == self.PRODUCTS_EDIT:
            self.product.edit()
        elif operation == self.PRODUCTS_REMOVE:
            self.product.remove()
        elif operation == self.PRODUCTS_UPDATE:
            self.product.update()
        elif operation == self.CATEG0RIES_INIT:
            self.category.get()
        elif operation == self.CATEGORIES_ADD:
            self.category.add()
        elif operation == self.CATEGORIES_EDIT:
            self.category.edit()
        elif operation == self.CATEGORIES_REMOVE:
            self.category.remove()
        elif operation == self.CATEGORIES_UPDATE:
            self.category.update()
