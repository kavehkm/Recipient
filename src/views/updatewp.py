# standard
from datetime import datetime
# internal
from src.worker import Worker
from src import db, wc, models, messages
from src.ui.windows import RegisterForm, OptionsList
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
            objects = [
                [getattr(obj, self.MODEL_ID), getattr(obj, self.MODEL_NAME), obj.wpid, obj.last_update]
                for obj in self._get_registered_objects()
            ]
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages[4], str(e))
            msg.show()
        else:
            self.table.setRecords(objects)

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
            self.form.setWpid(record[2])
            self.form.btnSave.clicked.connect(lambda: self.save(index))
            self.form.signals.showOptions.connect(self.show_options)
            self.form.show()

    def show_options(self, subject):
        try:
            if subject == self.form.ID:
                columns = ['ID', 'Name']
                title = self.messages[1]
                options = [
                    [getattr(obj, self.MODEL_ID), getattr(obj, self.MODEL_NAME)]
                    for obj in self._get_unregistered_moein_objects()
                ]
            else:
                columns = ['WPID', 'Name']
                title = self.messages[0]
                options = [
                    [obj[self.WPMODEL_ID], obj[self.WPMODEL_NAME]]
                    for obj in self._get_unregistered_wp_objects()
                ]
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

    def select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWpid(item[0])
        self.options_list.close()

    def save(self, index=None):
        try:
            # get moeinid and wpid from form
            moeinid = int(self.form.getId())
            wpid = int(self.form.getWpid())
            # check moeinid
            with db.connection() as conn:
                self.MODEL.connection = conn
                moein_object = self.MODEL.get(self.MODEL_NAME, **{self.MODEL_ID: moeinid})
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
                objects = self._get_unregistered_moein_objects()
                adder = self._moein_adder
            else:
                objects = self._get_unregistered_wp_objects()
                adder = self._wp_adder
        except Exception as e:
            msg = Message(self.options_list, Message.ERROR, self.messages[5], str(e))
            msg.show()
        else:
            if objects:
                pd = Progress(self.options_list, self.messages[8], 0, len(objects))
                pd.show()
                worker = Worker(adder, objects)
                worker.signals.progress.connect(pd.setValue)
                worker.signals.error.connect(pd.close)
                worker.signals.error.connect(self.add_all_error)
                worker.signals.done.connect(self.add_all_done)
                QThreadPool.globalInstance().start(worker)
                self.options_list.btnAddAll.setDisabled(True)

    def add_all_error(self, error):
        self.options_list.btnAddAll.setEnabled(True)
        msg = Message(self.options_list, Message.ERROR, self.messages[10], str(error))
        msg.show()

    def add_all_done(self):
        self.options_list.btnAddAll.setEnabled(True)
        msg = Message(self.options_list, Message.SUCCESS, self.messages[11])
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
                [], ['wpid', 'last_update', 'update_required']
            )
        return registered_objects

    def _get_unregistered_moein_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            unregistered_objects = self.MODEL.left_outer_join(
                self.MAP,
                self.MODEL_ID, 'id',
                []
            )
        return unregistered_objects

    def _get_unregistered_wp_objects(self):
        with db.connection() as conn:
            self.MAP.connection = conn
            ids = [i.wpid for i in self.MAP.all('wpid')]
        return self.WPMODEL.all(excludes=ids)

    def _wp_adder(self, objects, progress_callback):
        pass

    def _moein_adder(self, objects, progress_callback):
        pass

    def _updater(self, objects, progress_callback):
        pass


class ProductView(ObjectView):
    """Product View"""
    MAP = models.ProductMap()
    MODEL = models.Product()
    WPMODEL = wc.Product()
    MESSAGE_SLICE = slice(0, 19)

    def _wp_adder(self, wp_products, progress_callback):
        with db.connection() as conn:
            category_map = models.CategoryMap()
            self.MODEL.connection = self.MAP.connection = category_map.connection = conn
            for i, wp_product in enumerate(wp_products, 1):
                wp_category = wp_product['categories'][0]
                moein_category = category_map.get('id', wpid=wp_category['id'])
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
                conn.commit()
                progress_callback.emit(i)

    def _moein_adder(self, moein_products, progress_callback):
        with db.connection() as conn:
            category_map = models.CategoryMap()
            self.MAP.connection = category_map.connection = conn
            for i, moein_product in enumerate(moein_products, 1):
                wp_category = category_map.get('wpid', id=moein_product.category_id)
                wp_product = self.WPMODEL.create(
                    moein_product.name,
                    str(moein_product.price),
                    [wp_category.wpid]
                )
                self.MAP.create({
                    'id': moein_product.id,
                    'wpid': wp_product['id'],
                    'last_update': datetime.now()
                })
                conn.commit()
                progress_callback.emit(i)

    def _updater(self, moein_products, progress_callback):
        with db.connection() as conn:
            self.MAP.connection = conn
            for i, moein_product in enumerate(moein_products, 1):
                self.WPMODEL.update(moein_product.wpid, {
                    'name': moein_product.name,
                    'regular_price': str(moein_product.price)
                })
                self.MAP.update({'last_update': datetime.now()}, id=moein_product.id)
                conn.commit()
                progress_callback.emit(i)


class CategoryView(ObjectView):
    """Category View"""
    MAP = models.CategoryMap()
    MODEL = models.Category()
    WPMODEL = wc.Category()
    MESSAGE_SLICE = slice(19, 38)

    def _wp_adder(self, wp_categories, progress_callback):
        with db.connection() as conn:
            self.MODEL.connection = self.MAP.connection = conn
            for i, wp_category in enumerate(wp_categories, 1):
                self.MODEL.create({
                    'name': wp_category['name']
                })
                self.MAP.create({
                    'id': self.MODEL.get_max_pk(),
                    'wpid': wp_category['id'],
                    'last_update': datetime.now()
                })
                conn.commit()
                progress_callback.emit(i)

    def _moein_adder(self, moein_categories, progress_callback):
        with db.connection() as conn:
            self.MAP.connection = conn
            for i, moein_category in enumerate(moein_categories, 1):
                wp_category = self.WPMODEL.create(
                    moein_category.name
                )
                self.MAP.create({
                    'id': moein_category.id,
                    'wpid': wp_category['id'],
                    'last_update': datetime.now()
                })
                conn.commit()
                progress_callback.emit(i)

    def _updater(self, moein_categories, progress_callback):
        with db.connection() as conn:
            self.MAP.connection = conn
            for i, moein_category in enumerate(moein_categories, 1):
                self.WPMODEL.update(moein_category.wpid, {
                    'name': moein_category.name
                })
                self.MAP.update({'last_update': datetime.now()}, id=moein_category.id)
                conn.commit()
                progress_callback.emit(i)


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
