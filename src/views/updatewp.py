# standard
import time
from datetime import datetime
# internal
from src.worker import Worker
from src import db, models, wc, messages
from src.ui.windows import AddEditForm, AddEditOptions
from src.ui.components import Message, Confirm, Progress
# pyqt
from PyQt5.QtCore import QThreadPool


class ObjectView(object):
    """Object View"""
    # object related models and map
    MAP = None
    MODEL = None
    WPMODEL = None
    # object model columns
    MODEL_ID = 'id'
    MODEL_NAME = 'name'
    # object wpmodel columns
    WPMODEL_ID = 'id'
    WPMODEL_NAME = 'name'
    # messages slice
    MESSAGE_SLICE = slice(0, 0)

    def __init__(self, parent, table):
        self.parent = parent
        self.table = table
        self.ui = self.parent.ui
        self.tab = self.parent.tab
        self.messages = messages.get(self.MESSAGE_SLICE)

    def get(self):
        try:
            objects = self._get_registered_objects()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[4], str(e))
            msg.show()
        else:
            self.table.setRecords(objects)

    def add(self):
        self.form = AddEditForm(self.ui)
        self.form.setWindowTitle(self.messages[7])
        self.form.btnSave.clicked.connect(lambda: self.save())
        self.form.signals.showOptions.connect(self.show_options)
        self.form.show()

    def edit(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            record = self.table.getRecord(index)
            self.form = AddEditForm(self.ui)
            self.form.setWindowTitle(self.messages[6])
            self.form.setId(record[0])
            self.form.setWpid(record[2])
            self.form.btnSave.clicked.connect(lambda: self.save(index))
            self.form.signals.showOptions.connect(self.show_options)
            self.form.show()

    def show_options(self, subject):
        try:
            if subject == self.form.ID:
                columns = ['ID', 'Name']
                title = self.messages[1]
                options = self._get_moein_options()
            else:
                columns = ['WPID', 'Name']
                title = self.messages[0]
                options = self._get_wp_options()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages[3], str(e))
            msg.show()
        else:
            self.table_list = AddEditOptions(self.form, columns)
            self.table_list.setWindowTitle(title)
            self.table_list.setList(options)
            self.table_list.btnAddAll.clicked.connect(lambda: self.add_all(subject))
            self.table_list.signals.select.connect(lambda item: self.select_option(subject, item))
            self.table_list.show()

    def select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWpid(item[0])
        self.table_list.close()

    def save(self, index=None):
        try:
            # get moeinid and wpid from form
            moeinid = int(self.form.getId())
            wpid = int(self.form.getWpid())
            # check moeinid
            with db.connection() as conn:
                self.MODEL.connection = conn
                moein_object = self.MODEL.get(moeinid, self.MODEL_NAME)
                if moein_object is None:
                    raise Exception(self.messages[2])
            # check wpid
            self.WPMODEL.get(wpid)
            # everything is ok, lets register or update object
            with db.connection() as conn:
                self.MAP.connection = conn
                if index is None:
                    now = datetime.now()
                    self.MAP.create({'id': moeinid, 'wpid': wpid, 'last_update': now})
                else:
                    record = self.table.getRecord(index)
                    self.MAP.update({'id': moeinid, 'wpid': wpid}, id=record[0], wpid=record[2])
                # commit changes
                conn.commit()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages[14], str(e))
            msg.show()
        else:
            if index is None:
                self.table.addRecord([moeinid, getattr(moein_object, self.MODEL_NAME), wpid, now])
            else:
                record[0] = moeinid
                record[1] = getattr(moein_object, self.MODEL_NAME)
                record[2] = wpid
                self.table.updateRecord(index, record)
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, self.messages[15])
            msg.show()

    def add_all(self, subject):
        try:
            if subject == self.form.ID:
                objects = self._get_moein_options()
                adder = self._moein_adder
            else:
                objects = self._get_wp_options()
                adder = self._wp_adder
        except Exception as e:
            msg = Message(self.table_list, Message.ERROR, self.messages[5], str(e))
            msg.show()
        else:
            if objects:
                pd = Progress(self.table_list, self.messages[8], 0, len(objects))
                pd.show()
                worker = Worker(adder, objects)
                worker.signals.progress.connect(pd.setValue)
                worker.signals.error.connect(pd.close)
                worker.signals.error.connect(self.add_all_error)
                worker.signals.done.connect(self.add_all_done)
                QThreadPool.globalInstance().start(worker)
                self.table_list.btnAddAll.setDisabled(True)

    def add_all_error(self, error):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.ERROR, self.messages[10], str(error))
        msg.show()

    def add_all_done(self):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.SUCCESS, self.messages[11])
        msg.show()

    def update(self):
        try:
            objects = self._get_registered_objects()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[4], str(e))
            msg.show()
        else:
            if objects:
                pd = Progress(self.ui, self.messages[9], 0, len(objects))
                pd.show()
                worker = Worker(self._updater, objects)
                worker.signals.progress.connect(pd.setValue)
                worker.signals.error.connect(pd.close)
                worker.signals.error.connect(self.update_error)
                worker.signals.done.connect(self.update_done)
                QThreadPool.globalInstance().start(worker)
                self.tab.btnUpdateWP.setDisabled(True)

    def update_error(self, error):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.ui, Message.ERROR, self.messages[12], str(error))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.ui, Message.SUCCESS, self.messages[13])
        msg.show()

    def remove(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            cfm = Confirm(self.ui, Confirm.WARNING, self.messages[16])
            cfm.btnOk.clicked.connect(lambda: self.remove_confirm(index))
            cfm.show()

    def remove_confirm(self, index):
        try:
            # get moeinid
            moeinid = int(self.table.getRecord(index)[0])
            with db.connection() as conn:
                self.MAP.connection = conn
                self.MAP.delete(id=moeinid)
                conn.commit()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[17], str(e))
            msg.show()
        else:
            self.table.removeRecord(index)
            msg = Message(self.ui, Message.SUCCESS, self.messages[18])
            msg.show()

    def _get_registered_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            registered_objects = self.MODEL.inner_join(
                self.MAP,
                self.MODEL_ID, 'id',
                [self.MODEL_ID, self.MODEL_NAME], ['wpid', 'last_update']
            )
        return registered_objects

    def _get_moein_options(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            moein_options = self.MODEL.left_outer_join(
                self.MAP,
                self.MODEL_ID, 'id',
                [self.MODEL_ID, self.MODEL_NAME]
            )
        return moein_options

    def _get_wp_options(self):
        wp_objects = []
        registered_objects_ids = []
        with db.connection() as conn:
            self.MAP.connection = conn
            for registered_object in self.MAP.all('wpid'):
                registered_objects_ids.append(registered_object.wpid)
        for wp_object in self.WPMODEL.all(per_page=100).json():
            if wp_object[self.WPMODEL_ID] not in registered_objects_ids:
                wp_objects.append([wp_object[self.WPMODEL_ID], wp_object[self.WPMODEL_NAME]])
        return wp_objects

    def _wp_adder(self, objects, progress_callback):
        pass

    def _moein_adder(self, objects, progress_callback):
        pass

    def _updater(self, objects, progress_callback):
        for i, obj in enumerate(objects, 1):
            time.sleep(1)
            progress_callback.emit(i)


class ProductView(ObjectView):
    """Product View"""
    MAP = models.ProductMap()
    MODEL = models.Product()
    WPMODEL = wc.Product()
    MESSAGE_SLICE = slice(0, 19)

    def _wp_adder(self, products, progress_callback):
        with db.connection() as conn:
            category_map = models.CategoryMap()
            self.MODEL.connection = self.MAP.connection = category_map.connection = conn
            for i, p in enumerate(products, 1):
                wp_product = self.WPMODEL.get(p[0]).json()
                wp_category = wp_product['categories'][0]
                try:
                    moein_category = category_map.filter('id', wpid=wp_category['id'])[0]
                except IndexError:
                    raise Exception('Category `{}` does not exists in map table.'.format(wp_category['name']))
                self.MODEL.create({
                    'name': wp_product['name'],
                    'price': wp_product['regular_price'],
                    'category_id': moein_category.id
                })
                self.MAP.create({
                    'id': self.MODEL.get_max_pk(),
                    'wpid': wp_product['id'],
                    'last_update': datetime.now()
                })
                # commit changes
                conn.commit()
                # report progress
                progress_callback.emit(i)

    def _moein_adder(self, products, progress_callback):
        pass


class CategoryView(ObjectView):
    """Category View"""
    MAP = models.CategoryMap()
    MODEL = models.Category()
    WPMODEL = wc.Category()
    MESSAGE_SLICE = slice(19, 38)

    def _wp_adder(self, categories, progress_callback):
        with db.connection() as conn:
            self.MODEL.connection = self.MAP.connection = conn
            for i, c in enumerate(categories, 1):
                wp_category = self.WPMODEL.get(c[0]).json()
                self.MODEL.create({
                    'name': wp_category['name']
                })
                self.MAP.create({
                    'id': self.MODEL.get_max_pk(),
                    'wpid': wp_category['id'],
                    'last_update': datetime.now()
                })
                # commit changes
                conn.commit()
                # report progress status
                progress_callback.emit(i)

    def _moein_adder(self, categories, progress_callback):
        pass


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
        self.product = ProductView(self, self.tab.productsTable)
        self.category = CategoryView(self, self.tab.categoriesTable)
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
