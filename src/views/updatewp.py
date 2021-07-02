# standard
import time
from datetime import datetime
# internal
from src import db
from src.worker import Worker
from src.ui.windows import AddEditForm, AddEditOptions
from src.ui.components import Message, Confirm, Progress
# models
from src import models
# wc
from src import wc
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
    # object names
    OBJECT_NAME = 'Object'
    OBJECT_NAME_PLURAL = 'Objects'

    def __init__(self, parent, ui, tab, table):
        self.parent = parent
        self.ui = ui
        self.tab = tab
        self.table = table
        self._messages = None

    @property
    def messages(self):
        if self._messages is None:
            self._messages = {
                # not found
                'object_notfound':          f'{self.OBJECT_NAME} Not Found.',
                # get
                'get_options_fail':         'Cannot Load Options.',
                'get_registered_fail':      f'Cannot Load Registered {self.OBJECT_NAME_PLURAL}.',
                'get_unregistered_fail':    f'Cannot Load Unregistered {self.OBJECT_NAME_PLURAL}.',
                # form title
                'edit_form_title':          f'Edit {self.OBJECT_NAME}',
                'add_form_title':           f'Add New {self.OBJECT_NAME}',
                # progress dialog
                'add_all_pd_title':         f'Add All {self.OBJECT_NAME_PLURAL}...',
                'update_pd_title':          f'Update All {self.OBJECT_NAME_PLURAL}...',
                # add all
                'add_all_fail':             f'Cannot Add All {self.OBJECT_NAME_PLURAL}.',
                'add_all_success':          f'All {self.OBJECT_NAME_PLURAL} Added Successfully.',
                # update
                'update_fail':              f'Cannot Update All {self.OBJECT_NAME_PLURAL}.',
                'update_success':           f'All {self.OBJECT_NAME_PLURAL} Updated Successfully.',
                # save
                'save_fail':                f'Cannot Save {self.OBJECT_NAME}.',
                'save_success':             f'{self.OBJECT_NAME} Saved Successfully.',
                # remove
                'remove_confirm':           'Are You Sure?',
                'remove_fail':              f'Cannot Remove {self.OBJECT_NAME}.',
                'remove_success':           f'{self.OBJECT_NAME} Removed Successfully.'
            }
        return self._messages

    def get(self):
        try:
            objects = self._get_registered_objects()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages['get_registered_fail'], str(e))
            msg.show()
        else:
            self.table.setRecords(objects)

    def add(self):
        self.form = AddEditForm(self.ui)
        self.form.setWindowTitle(self.messages['add_form_title'])
        self.form.btnSave.clicked.connect(self.add_save)
        self.form.signals.showOptions.connect(self.add_edit_show_options)
        self.form.show()

    def add_edit_show_options(self, subject):
        try:
            if subject == self.form.ID:
                columns = ['ID', 'Name']
                title = 'Moein {}'.format(self.OBJECT_NAME_PLURAL)
                options = self._get_unregistered_moein_objects()
            else:
                columns = ['WPID', 'Name']
                title = 'WP {}'.format(self.OBJECT_NAME_PLURAL)
                options = self._get_unregistered_wp_objects()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages['get_options_fail'], str(e))
            msg.show()
        else:
            self.table_list = AddEditOptions(self.form, columns)
            self.table_list.setWindowTitle(title)
            self.table_list.setList(options)
            self.table_list.btnAddAll.clicked.connect(lambda: self.add_all(subject))
            self.table_list.signals.select.connect(lambda item: self.add_edit_select_option(subject, item))
            self.table_list.show()

    def add_all(self, subject):
        try:
            if subject == self.form.ID:
                objects = self._get_unregistered_moein_objects()
                adder = self._adder
            else:
                objects = self._get_unregistered_wp_objects()
                adder = self._adder
        except Exception as e:
            msg = Message(self.table_list, Message.ERROR, self.messages['get_unregistered_fail'], str(e))
            msg.show()
        else:
            if objects:
                pd = Progress(self.table_list, self.messages['add_all_pd_title'], 0, len(objects))
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
        msg = Message(self.table_list, Message.ERROR, self.messages['add_all_fail'], str(error))
        msg.show()

    def add_all_done(self):
        self.table_list.btnAddAll.setEnabled(True)
        msg = Message(self.table_list, Message.SUCCESS, self.messages['add_all_success'])
        msg.show()

    def add_edit_select_option(self, subject, item):
        if subject == self.form.ID:
            self.form.setId(item[0])
        else:
            self.form.setWpid(item[0])
        self.table_list.close()

    def add_save(self):
        try:
            # get ids from form
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            # create database connection
            with db.connection() as conn:
                # set model connection
                self.MODEL.connection = self.MAP.connection = conn
                # get object from database by given moein_id
                obj = self.MODEL.get(moein_id, self.MODEL_NAME)
                if obj is None:
                    raise Exception(self.messages['object_notfound'])
                #
                # get wp_object from store by given wp_id
                #
                current_datetime = datetime.now()
                self.MAP.create({'id': moein_id, 'wpid': wp_id, 'last_update': current_datetime})
                conn.commit()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages['save_fail'], str(e))
            msg.show()
        else:
            self.form.close()
            self.table.addRecord([moein_id, getattr(obj, self.MODEL_NAME), wp_id, current_datetime])
            msg = Message(self.ui, Message.SUCCESS, self.messages['save_success'])
            msg.show()

    def edit(self):
        obj_index = self.table.getCurrentRecordIndex()
        if obj_index is not None:
            obj = self.table.getRecord(obj_index)
            self.form = AddEditForm(self.ui)
            self.form.setWindowTitle(self.messages['edit_form_title'])
            self.form.setId(obj[0])
            self.form.setWpid(obj[2])
            self.form.btnSave.clicked.connect(lambda: self.edit_save(obj_index))
            self.form.signals.showOptions.connect(self.add_edit_show_options)
            self.form.show()

    def edit_save(self, obj_index):
        try:
            moein_id = int(self.form.getId())
            wp_id = int(self.form.getWpid())
            obj_record = self.table.getRecord(obj_index)
            with db.connection() as conn:
                self.MODEL.connection = self.MAP.connection = conn
                obj = self.MODEL.get(moein_id, self.MODEL_NAME)
                if obj is None:
                    raise Exception(self.messages['object_notfound'])
                self.MAP.update({'id': moein_id, 'wpid': wp_id}, id=obj_record[0], wpid=obj_record[2])
                conn.commit()
        except Exception as e:
            msg = Message(self.form, Message.ERROR, self.messages['save_fail'], str(e))
            msg.show()
        else:
            obj_record[0] = moein_id
            obj_record[1] = getattr(obj, self.MODEL_NAME)
            obj_record[2] = wp_id
            self.table.updateRecord(obj_index, obj_record)
            self.form.close()
            msg = Message(self.ui, Message.SUCCESS, self.messages['save_success'])
            msg.show()

    def update(self):
        try:
            objects = self._get_registered_objects()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages['get_registered_fail'], str(e))
            msg.show()
        else:
            if objects:
                pd = Progress(self.ui, self.messages['update_pd_title'], 0, len(objects))
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
        msg = Message(self.ui, Message.ERROR, self.messages['update_fail'], str(error))
        msg.show()

    def update_done(self):
        self.tab.btnUpdateWP.setEnabled(True)
        msg = Message(self.ui, Message.SUCCESS, self.messages['update_success'])
        msg.show()

    def remove(self):
        obj_index = self.table.getCurrentRecordIndex()
        if obj_index is not None:
            cfm = Confirm(self.ui, Confirm.WARNING, self.messages['remove_confirm'])
            cfm.btnOk.clicked.connect(lambda: self.remove_confirm(obj_index))
            cfm.show()

    def remove_confirm(self, obj_index):
        try:
            # get object id
            moein_id = int(self.table.getRecord(obj_index)[0])
            # create connection to database
            with db.connection() as conn:
                # set connection
                self.MAP.connection = conn
                # delete registered object from map table
                self.MAP.delete(id=moein_id)
                conn.commit()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, self.messages['remove_fail'], str(e))
            msg.show()
        else:
            self.table.removeRecord(obj_index)
            msg = Message(self.ui, Message.SUCCESS, self.messages['remove_success'])
            msg.show()

    ##########################
    # overwrite this methods #
    ##########################
    def _get_registered_objects(self):
        """
        Get all moein-objects that inner joined with map table

        :return: registered moein-objects
        :rtype: list
        """
        return []

    def _get_unregistered_moein_objects(self):
        """
        Get all moein-objects that right outer joined with map table

        :return: unregistered moein-objects
        :rtype: list
        """
        return []

    def _get_unregistered_wp_objects(self):
        """
        Get all wp-objects that not registered in map table

        :return: unregistered wp-objects
        :rtype: list
        """
        return []

    @staticmethod
    def _adder(objects, progress_callback):
        """
        Register objects in map table and also add them to wp store

        :param list objects: unregistered moein-objects
        :param pyqtSignal progress_callback: progress reporting signal
        """

    @staticmethod
    def _updater(objects, progress_callback):
        """
        Update all registered objects on wp store from map table

        :param list objects: registered moein-objects
        :param pyqtSignal progress_callback: progress reporting signal
        """


class ProductView(ObjectView):
    """Product View"""
    MAP = models.ProductMap()
    MODEL = models.Product()
    WPMODEL = wc.Product()
    OBJECT_NAME = 'Product'
    OBJECT_NAME_PLURAL = 'Products'

    def _get_registered_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            registered_products = self.MODEL.inner_join(self.MAP, 'id', 'id', ['id', 'name'], ['wpid', 'last_update'])
        return registered_products

    def _get_unregistered_moein_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            unregistered_products = self.MODEL.left_outer_join(self.MAP, 'id', 'id', ['id', 'name'])
        return unregistered_products

    def _get_unregistered_wp_objects(self):
        return [[i, f'WP Product{i}'] for i in range(10)]

    @staticmethod
    def _adder(products, progress_callback):
        for i, product in enumerate(products, 1):
            time.sleep(0.1)
            progress_callback.emit(i)

    @staticmethod
    def _updater(products, progress_callback):
        for i, products in enumerate(products, 1):
            time.sleep(0.5)
            progress_callback.emit(i)


class CategoryView(ObjectView):
    """Category View"""
    MAP = models.CategoryMap()
    MODEL = models.Category()
    WPMODEL = wc.Category()
    OBJECT_NAME = 'Category'
    OBJECT_NAME_PLURAL = 'Categories'

    def _get_registered_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            registered_categories = self.MODEL.inner_join(self.MAP, 'id', 'id', ['id', 'name'], ['wpid', 'last_update'])
        return registered_categories

    def _get_unregistered_moein_objects(self):
        with db.connection() as conn:
            self.MODEL.connection = conn
            unregistered_categories = self.MODEL.left_outer_join(self.MAP, 'id', 'id', ['id', 'name'])
        return unregistered_categories

    def _get_unregistered_wp_objects(self):
        return [[i, f'WP Category{i}'] for i in range(5)]

    @staticmethod
    def _adder(categories, progress_callback):
        for i, category in enumerate(categories, 1):
            time.sleep(2)
            progress_callback.emit(i)

    @staticmethod
    def _updater(categories, progress_callback):
        for i, category in enumerate(categories, 1):
            time.sleep(2)
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
        self.product = ProductView(self, self.ui, self.tab, self.tab.productsTable)
        self.category = CategoryView(self, self.ui, self.tab, self.tab.categoriesTable)
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
