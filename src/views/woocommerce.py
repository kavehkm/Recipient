# internal
from src import messages
from src import connection
from src.worker import Worker
from src.models import Category, Product
from src.ui.windows import RegisterForm, OptionsList
from src.ui.components import Message, Confirm, Progress
# pyqt
from PyQt5.QtCore import QThreadPool


class ObjectView(object):
    """Object View"""
    # related object
    model = None
    # message slice
    message_slice = slice(0, 0)

    def __init__(self, parent, table):
        self.parent = parent
        self.table = table
        self.ui = self.parent.ui
        self.tab = self.parent.tab
        self.messages = messages.get(self.message_slice)

    def get(self):
        # create and set connection
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            mapped = [
                [m['id'], m['name'], m['wcid'], m['last_update']]
                for m in self.model.mapped()
            ]
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[4], str(e))
            msg.show()
        else:
            self.table.setRecords(mapped)
        finally:
            conn.close()

    def add(self):
        self.form = RegisterForm(self.ui)
        self.form.setWindowTitle(self.messages[7])
        self.form.btnSave.clicked.connect(lambda: self.save())
        self.form.signals.showOptions.connect(self.show_options)
        self.form.show()

    def edit(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            record = self.table.getRecord(index)
            self.form = RegisterForm(self.ui)
            self.form.setWindowTitle(self.messages[6])
            self.form.setId(record[0])
            self.form.setWcid(record[2])
            self.form.btnSave.clicked.connect(lambda: self.save(index))
            self.form.signals.showOptions.connect(self.show_options)
            self.form.show()

    def show_options(self, subject):
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            if subject == self.form.ID:
                columns = ['ID', 'Name']
                title = self.messages[1]
                options = [[um['id'], um['name']] for um in self.model.unmapped()]
            else:
                columns = ['WCID', 'Name']
                title = self.messages[0]
                options = [[um['id'], um['name']] for um in self.model.wc_unmapped()]
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages[3], str(e))
            msg.show()
        else:
            self.options_list = OptionsList(self.form, columns)
            self.options_list.setWindowTitle(title)
            self.options_list.setList(options)
            self.options_list.btnAddAll.clicked.connect(lambda: self.add_all(subject))
            self.options_list.signals.select.connect(lambda item: self.select_option(subject, item))
            self.options_list.show()
        finally:
            conn.close()

    def select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWcid(item[0])
        self.options_list.close()

    def save(self, index=None):
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            moeinid = int(self.form.getId())
            wcid = int(self.form.getWcid())
            if index is None:
                new_map = self.model.add_map(moeinid, wcid)
                self.table.addRecord([
                    new_map['id'],
                    new_map['name'],
                    new_map['wcid'],
                    new_map['last_update']
                ])
            else:
                record = self.table.getRecord(index)
                edited_map = self.model.edit_map(record[0], moeinid, wcid)
                self.table.updateRecord(
                    index,
                    [edited_map['id'],
                     edited_map['name'],
                     edited_map['wcid'],
                     record[3]]
                )
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages[14], str(e))
            msg.show()
        else:
            conn.commit()
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, self.messages[15])
            msg.show()
        finally:
            conn.close()

    def add_all(self, subject):
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            if subject == self.form.ID:
                unmapped = self.model.unmapped()
                adder = self.wc_adder
            else:
                unmapped = self.model.wc_unmapped()
                adder = self.moein_adder
        except Exception as e:
            msg = Message(self.options_list, Message.ERROR, self.messages[5], str(e))
            msg.show()
        else:
            if unmapped:
                pd = Progress(self.options_list, self.messages[8], 0, len(unmapped))
                pd.show()
                worker = Worker(adder, unmapped)
                worker.signals.progress.connect(pd.setValue)
                worker.signals.error.connect(pd.close)
                worker.signals.error.connect(self.add_all_error)
                worker.signals.done.connect(self.add_all_done)
                QThreadPool.globalInstance().start(worker)
                self.options_list.btnAddAll.setDisabled(True)
        finally:
            conn.close()

    def moein_adder(self, unmapped, progress_callback):
        error = None
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            for i, um in enumerate(unmapped, 1):
                self.model.import2moein(um)
                conn.commit()
                progress_callback.emit(i)
        except Exception as e:
            conn.rollback()
            error = e
        conn.close()
        if error:
            raise error

    def wc_adder(self, unmapped, progress_callback):
        error = None
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            for i, um in enumerate(unmapped, 1):
                self.model.export2wc(um)
                conn.commit()
                progress_callback.emit(i)
        except Exception as e:
            conn.rollback()
            error = e
        conn.close()
        if error:
            raise error

    def add_all_error(self, error):
        self.options_list.btnAddAll.setEnabled(True)
        msg = Message(self.options_list, Message.ERROR, self.messages[10], str(error))
        msg.show()

    def add_all_done(self):
        self.options_list.btnAddAll.setEnabled(True)
        msg = Message(self.options_list, Message.SUCCESS, self.messages[11])
        msg.show()

    def update(self):
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            mapped = self.model.mapped(update_required=True)
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[4], str(e))
            msg.show()
        else:
            if mapped:
                pd = Progress(self.ui, self.messages[9], 0, len(mapped))
                pd.show()
                worker = Worker(self.updater, mapped)
                worker.signals.progress.connect(pd.setValue)
                worker.signals.error.connect(pd.close)
                worker.signals.error.connect(self.update_error)
                worker.signals.done.connect(self.update_done)
                QThreadPool.globalInstance().start(worker)
                self.tab.btnUpdate.setDisabled(True)
        finally:
            conn.close()

    def updater(self, mapped, progress_callback):
        error = None
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            for i, m in enumerate(mapped, 1):
                self.model.wc_mapped_update(m)
                conn.commit()
                progress_callback.emit(i)
        except Exception as e:
            conn.rollback()
            error = e
        conn.close()
        if error:
            raise error

    def update_error(self, error):
        self.tab.btnUpdate.setEnabled(True)
        msg = Message(self.ui, Message.ERROR, self.messages[12], str(error))
        msg.show()

    def update_done(self):
        self.tab.btnUpdate.setEnabled(True)
        msg = Message(self.ui, Message.SUCCESS, self.messages[13])
        msg.show()

    def remove(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            cfm = Confirm(self.ui, Confirm.WARNING, self.messages[16])
            cfm.btnOk.clicked.connect(lambda: self.remove_confirm(index))
            cfm.show()

    def remove_confirm(self, index):
        conn = connection.get()
        self.model.set_connection(conn)
        try:
            moeinid = int(self.table.getRecord(index)[0])
            self.model.remove_map(moeinid)
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[17], str(e))
            msg.show()
        else:
            conn.commit()
            self.table.removeRecord(index)
            msg = Message(self.ui, Message.SUCCESS, self.messages[18])
            msg.show()
        finally:
            conn.close()


class ProductView(ObjectView):
    """Product View"""
    model = Product()
    message_slice = slice(0, 19)


class CategoryView(ObjectView):
    """Category View"""
    model = Category()
    message_slice = slice(19, 38)


class WooCommerce(object):
    """WooCommerce View"""
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
        self.tab = ui.contents.woocommerce
        # attach views
        self.product = ProductView(self, self.tab.productsTable)
        self.category = CategoryView(self, self.tab.categoriesTable)
        # connect signals
        self.ui.menu.btnWooCommerce.clicked.connect(self.tab_handler)
        self.tab.tabs.currentChanged.connect(lambda: self.dispatcher(self.INIT))
        self.tab.btnAdd.clicked.connect(lambda: self.dispatcher(self.ADD))
        self.tab.btnEdit.clicked.connect(lambda: self.dispatcher(self.EDIT))
        self.tab.btnRemove.clicked.connect(lambda: self.dispatcher(self.REMOVE))
        self.tab.btnUpdate.clicked.connect(lambda: self.dispatcher(self.UPDATE))

    def tab_handler(self):
        self.dispatcher(self.INIT)
        self.ui.contents.showTab(self.ui.contents.WOOCOMMERCE)

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
