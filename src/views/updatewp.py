# standard
import random
from datetime import datetime
# internal
from src.ui.widgets import Message


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
        # dispatch signal to proper method
        if operation == self.PRODUCTS_INIT:
            self.init_products()
        elif operation == self.PRODUCTS_ADD:
            self.add_product()
        elif operation == self.PRODUCTS_EDIT:
            self.edit_product()
        elif operation == self.PRODUCTS_REMOVE:
            self.remove_product()
        elif operation == self.PRODUCTS_UPDATE:
            self.update_products()
        elif operation == self.CATEG0RIES_INIT:
            self.init_categories()
        elif operation == self.CATEGORIES_ADD:
            self.add_category()
        elif operation == self.CATEGORIES_EDIT:
            self.edit_category()
        elif operation == self.CATEGORIES_REMOVE:
            self.remove_category()
        elif operation == self.CATEGORIES_UPDATE:
            self.update_categories()

    def init_products(self):
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
        self.tab.productsTable.setRecords(products)

    def add_product(self):
        random_int = random.randint(1, 10000)
        new_product = [
            random_int,
            random_int + 1,
            f'Product{random_int}',
            random_int * 2,
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.tab.productsTable.addRecord(new_product)
        msg = Message(self.tab, Message.SUCCESS, 'New Product Added Successfully')
        msg.show()

    def edit_product(self):
        product_index = self.tab.productsTable.getCurrentRecordIndex()
        if product_index is not None:
            product = self.tab.productsTable.getRecord(product_index)
            product[2] = product[2] + '-edited'
            self.tab.productsTable.updateRecord(product_index, product)
            msg = Message(self.tab, Message.SUCCESS, 'Product Updated Successfully.')
            msg.show()

    def remove_product(self):
        product_index = self.tab.productsTable.getCurrentRecordIndex()
        if product_index is not None:
            self.tab.productsTable.removeRecord(product_index)
            msg = Message(self.tab, Message.SUCCESS, 'Product Removed Successfully.')
            msg.show()

    @staticmethod
    def update_products():
        print('update products on wordpress')

    def init_categories(self):
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
        self.tab.categoriesTable.setRecords(categories)

    def add_category(self):
        random_int = random.randint(1, 10000)
        new_category = [
            random_int,
            f'Category{random_int}',
            random_int * 2,
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.tab.categoriesTable.addRecord(new_category)
        msg = Message(self.tab, Message.SUCCESS, 'New Category Added Successfully')
        msg.show()

    def edit_category(self):
        category_index = self.tab.categoriesTable.getCurrentRecordIndex()
        if category_index is not None:
            category = self.tab.categoriesTable.getRecord(category_index)
            category[1] = category[1] + '-edited'
            self.tab.categoriesTable.updateRecord(category_index, category)
            msg = Message(self.tab, Message.SUCCESS, 'Category Updated Successfully.')
            msg.show()

    def remove_category(self):
        category_index = self.tab.categoriesTable.getCurrentRecordIndex()
        if category_index is not None:
            self.tab.categoriesTable.removeRecord(category_index)
            msg = Message(self.tab, Message.SUCCESS, 'Category Removed Successfully.')
            msg.show()

    @staticmethod
    def update_categories():
        print('update categories on wordpress')
