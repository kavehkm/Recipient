# standard
import time
import random
from datetime import datetime
# internal
from src import db
from src.worker import Worker
from src.ui.windows import AddEditForm, AddEditOptions
from src.ui.components import Message, Confirm, Progress
# models
from src.models import Product, ProductMap, Category, CategoryMap
# pyqt
from PyQt5.QtCore import QThreadPool


class ProductView(object):
    """Product View"""
    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.tab = parent.tab
        self.table = parent.tab.productsTable

    def get(self):
        try:
            # create connection to database
            conn = db.connection()
            # create needed models
            p, pm = Product(), ProductMap()
            # set connection for query
            p.connection = conn
            # get registered products by inner join on ProductMap
            registered_products = p.inner_join(pm, 'id', 'id', ['id', 'name'], ['wpid', 'last_update'])
            conn.close()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, 'Cannot Load Registered Products From Database.', str(e))
            msg.show()
        else:
            self.table.setRecords(registered_products)

    def add(self):
        self.form = AddEditForm(self.ui)
        self.form.setWindowTitle('Add New Product')
        self.form.btnSave.clicked.connect(self.add_save)
        self.form.signals.showOptions.connect(self.add_edit_show_options)
        self.form.show()

    def add_edit_show_options(self, subject):
        try:
            if subject == self.form.ID:
                conn = db.connection()
                p, pm = Product(), ProductMap()
                p.connection = conn
                items = p.left_outer_join(pm, 'id', 'id', ['id', 'name'])
                title = 'Moein Products'
                columns = ['ID', 'Name']
                conn.close()
            else:
                items = [
                    [i, f'WP Product{i}']
                    for i in range(10)
                ]
                title = 'WP Products'
                columns = ['WPID', 'Name']
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Load Options', str(e))
            msg.show()
        else:
            self.table_list = AddEditOptions(self.form, columns)
            self.table_list.setWindowTitle(title)
            self.table_list.setList(items)
            self.table_list.btnAddAll.clicked.connect(lambda: self.add_all(subject))
            self.table_list.signals.select.connect(lambda item: self.add_edit_select_option(subject, item))
            self.table_list.show()

    def add_all(self, subject):
        if subject == self.form.ID:
            products = [i for i in range(100)]
            pd = Progress(self.table_list, 'Add All Products', 0, len(products))
            worker = Worker(self.adder, products)
            worker.signals.progress.connect(pd.setValue)
            worker.signals.error.connect(pd.close)
            worker.signals.error.connect(self.add_all_error)
            worker.signals.done.connect(self.add_all_done)
            QThreadPool.globalInstance().start(worker)
            self.table_list.btnAddAll.setDisabled(True)

    @staticmethod
    def adder(products, progress_callback):
        for i, product in enumerate(products, 1):
            time.sleep(0.1)
            progress_callback.emit(i)

    def add_all_error(self, e):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.ERROR, 'Cannot Add All Products.', str(e))
        msg.show()

    def add_all_done(self):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.SUCCESS, 'All Products Added Successfully.')
        msg.show()

    def add_edit_select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWpid(item[0])
        self.table_list.close()

    def add_save(self):
        try:
            # get ids from form and convert into integer
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            # create connection to database
            conn = db.connection()
            # create needed models
            p, pm = Product(), ProductMap()
            # set connection
            p.connection = pm.connection = conn
            # get product from database by id
            product = p.get(moein_id, 'id', 'name')
            # check: if product does not exists raise Exception
            if product is None:
                raise Exception('Product Not Found.')
            # get wp product from woocommerce
            # ...
            # register product with wp product into map table
            current_datetime = datetime.now()
            pm.create({'id': product.id, 'wpid': wp_id, 'last_update': current_datetime})
            conn.commit()
            conn.close()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Add New Product', str(e))
        else:
            self.table.addRecord([product.id, product.name, wp_id, current_datetime])
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, 'New Product Added Successfully.')
        msg.show()

    def edit(self):
        product_index = self.table.getCurrentRecordIndex()
        if product_index is not None:
            product = self.table.getRecord(product_index)
            self.form = AddEditForm(self.ui)
            self.form.setWindowTitle('Edit Product')
            self.form.setId(product[0])
            self.form.setWpid(product[2])
            self.form.btnSave.clicked.connect(lambda: self.edit_save(product_index))
            self.form.signals.showOptions.connect(self.add_edit_show_options)
            self.form.show()

    def edit_save(self, product_index):
        try:
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            product = self.table.getRecord(product_index)
            product[0] = moein_id
            product[2] = wp_id
            self.table.updateRecord(product_index, product)
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Edit Product.', str(e))
        else:
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, 'Product Edited Successfully.')
        msg.show()

    def remove(self):
        product_index = self.table.getCurrentRecordIndex()
        if product_index is not None:
            cfm = Confirm(self.ui, Confirm.WARNING, 'Are You Sure?')
            cfm.btnOk.clicked.connect(lambda: self.confirm_remove(product_index))
            cfm.show()

    def confirm_remove(self, product_index):
        try:
            # get product id
            moein_id = int(self.table.getRecord(product_index)[0])
            # create connection to database
            conn = db.connection()
            # create needed model
            pm = ProductMap()
            # set connection
            pm.connection = conn
            # delete registered product from map table
            pm.delete(id=moein_id)
            conn.commit()
            conn.close()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, 'Cannot Remove Product From Map Table.', str(e))
        else:
            self.table.removeRecord(product_index)
            msg = Message(self.ui, Message.SUCCESS, 'Product Removed Successfully.')
        msg.show()

    def update(self):
        # query database
        products = [i for i in range(50)]
        # progress dialog
        pd = Progress(self.ui, 'Update Products...', 0, len(products))
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
        msg = Message(self.ui, Message.ERROR, 'Cannot Update Products.', str(e))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.ui, Message.SUCCESS, 'Products Updated Successfully.')
        msg.show()


class CategoryView(object):
    """Category View"""
    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.tab = parent.tab
        self.table = parent.tab.categoriesTable

    def get(self):
        try:
            # create connection to database
            conn = db.connection()
            # create needed models
            c, cm = Category(), CategoryMap()
            # set connection for query
            c.connection = conn
            # get registered categories by inner join on CategoryMap
            registered_categories = c.inner_join(cm, 'id', 'id', ['id', 'name'], ['wpid', 'last_update'])
            conn.close()
            self.table.setRecords(registered_categories)
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, 'Cannot Load Registered Categories From Database', str(e))
            msg.show()

    def add(self):
        self.form = AddEditForm(self.ui)
        self.form.setWindowTitle('Add New Category')
        self.form.btnSave.clicked.connect(self.add_save)
        self.form.signals.showOptions.connect(self.add_edit_show_options)
        self.form.show()

    def add_edit_show_options(self, subject):
        try:
            if subject == self.form.ID:
                conn = db.connection()
                c, cm = Category(), CategoryMap()
                c.connection = conn
                items = c.left_outer_join(cm, 'id', 'id', ['id', 'name'])
                title = 'Moein Categories'
                columns = ['ID', 'Name']
                conn.close()
            else:
                items = [
                    [i, f'WP Category{i}']
                    for i in range(5)
                ]
                title = 'WP Categories'
                columns = ['WPID', 'Name']
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Load Options', str(e))
            msg.show()
        else:
            self.table_list = AddEditOptions(self.form, columns)
            self.table_list.setWindowTitle(title)
            self.table_list.setList(items)
            self.table_list.btnAddAll.clicked.connect(lambda: self.add_all(subject))
            self.table_list.signals.select.connect(lambda item: self.add_edit_select_option(subject, item))
            self.table_list.show()

    def add_all(self, subject):
        if subject == self.form.ID:
            categories = [i for i in range(100)]
            pd = Progress(self.table_list, 'Add All Categories', 0, len(categories))
            worker = Worker(self.adder, categories)
            worker.signals.progress.connect(pd.setValue)
            worker.signals.error.connect(pd.close)
            worker.signals.error.connect(self.add_all_error)
            worker.signals.done.connect(self.add_all_done)
            QThreadPool.globalInstance().start(worker)
            self.table_list.btnAddAll.setDisabled(True)

    @staticmethod
    def adder(categories, progress_callback):
        for i, category in enumerate(categories, 1):
            time.sleep(0.1)
            progress_callback.emit(i)

    def add_all_error(self):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.ERROR, 'Cannot Add All Categories', str(e))
        msg.show()

    def add_all_done(self):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.SUCCESS, 'All Categories Added Successfully.')
        msg.show()

    def add_edit_select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWpid(item[0])
        self.table_list.close()

    def add_save(self):
        try:
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            conn = db.connection()
            c, cm = Category(), CategoryMap()
            c.connection = cm.connection = conn
            category = c.get(moein_id, 'id', 'name')
            if category is None:
                raise Exception('Category Not Found.')
            current_datetime = datetime.now()
            cm.create({'id': category.id, 'wpid': wp_id, 'last_update': current_datetime})
            conn.commit()
            conn.close()
            self.table.addRecord([category.id, category.name, wp_id, current_datetime])
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Add New Category')
        else:
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, 'New Category Added Successfully.')
        msg.show()

    def edit(self):
        category_index = self.table.getCurrentRecordIndex()
        if category_index is not None:
            category = self.table.getRecord(category_index)
            self.form = AddEditForm(self.ui)
            self.form.setWindowTitle('Edit Category')
            self.form.setId(category[0])
            self.form.setWpid(category[2])
            self.form.btnSave.clicked.connect(lambda: self.edit_save(category_index))
            self.form.signals.showOptions.connect(self.add_edit_show_options)
            self.form.show()

    def edit_save(self, category_index):
        try:
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            category = self.table.getRecord(category_index)
            category[0] = moein_id
            category[2] = wp_id
            self.table.updateRecord(category_index, category)
        except Exception as e:
            msg = Message(self.form, Message.ERROR, 'Cannot Edit Category.', str(e))
        else:
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, 'Category Edited Success')
        msg.show()

    def remove(self):
        category_index = self.table.getCurrentRecordIndex()
        if category_index is not None:
            cfm = Confirm(self.ui, Confirm.WARNING, 'Are You Sure?')
            cfm.btnOk.clicked.connect(lambda: self.confirm_remove(category_index))
            cfm.show()

    def confirm_remove(self, category_index):
        try:
            moein_id = int(self.table.getRecord(category_index)[0])
            conn = db.connection()
            cm = CategoryMap()
            cm.connection = conn
            cm.delete(id=moein_id)
            conn.commit()
            conn.close()
            self.table.removeRecord(category_index)
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, 'Cannot Remove Category From Map Table.', str(e))
        else:
            msg = Message(self.ui, Message.SUCCESS, 'Product Removed Successfully.')
        msg.show()

    def update(self):
        # query database
        categories = [i for i in range(10)]
        # progress dialog
        pd = Progress(self.ui, 'Update Categories...', 0, len(categories))
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
        msg = Message(self.ui, Message.ERROR, 'Cannot Update Categories.', str(e))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.ui, Message.SUCCESS, 'Categories Updated Successfully.')
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
    CATEGORIES_INIT = CATEGORIES + INIT
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
        elif operation == self.CATEGORIES_INIT:
            self.category.get()
        elif operation == self.CATEGORIES_ADD:
            self.category.add()
        elif operation == self.CATEGORIES_EDIT:
            self.category.edit()
        elif operation == self.CATEGORIES_REMOVE:
            self.category.remove()
        elif operation == self.CATEGORIES_UPDATE:
            self.category.update()
