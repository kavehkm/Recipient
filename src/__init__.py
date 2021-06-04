# standard
import random
from datetime import datetime
# internal
from src import settings as s
from src.ui.widgets import Message


class Controller(object):
    """Controller"""
    def __init__(self, ui):
        self.ui = ui
        # ui alias
        self.ui_status = self.ui.contents.status
        self.ui_invoices = self.ui.contents.invoices
        self.ui_updateWP = self.ui.contents.updateWP
        self.ui_settings = self.ui.contents.settings
        self.ui_logs = self.ui.contents.logs
        self.ui_help = self.ui.contents.help
        self.ui_about = self.ui.contents.about
        # bootstrap
        self.bootstrap()

    def bootstrap(self):
        self.connect_signals()

    def connect_signals(self):
        # menu buttons
        self.ui.menu.btnStatus.clicked.connect(self.status_handler)
        self.ui.menu.btnInvoices.clicked.connect(self.invoices_handler)
        self.ui.menu.btnUpdateWP.clicked.connect(self.updateWP_handler)
        self.ui.menu.btnSettings.clicked.connect(self.settings_handler)
        self.ui.menu.btnLogs.clicked.connect(self.logs_handler)
        self.ui.menu.btnHelp.clicked.connect(self.help_handler)
        self.ui.menu.btnAbout.clicked.connect(self.about_handler)
        # contents: status tab
        self.ui_status.btnStart.clicked.connect(self.status_btnStart_handler)
        self.ui_status.btnStop.clicked.connect(self.status_btnStop_handler)
        # contents: settings tab
        self.ui_settings.btnSave.clicked.connect(self.settings_btnSave_handler)
        self.ui_settings.btnClear.clicked.connect(self.settings_btnClear_handler)
        # contents: updateWP tab
        self.ui_updateWP.tabs.currentChanged.connect(self.updateWP_tabs_handler)
        self.ui_updateWP.signalAction.connect(self.updateWP_action_dispatcher)

    ###################
    # status handlers #
    ###################
    def status_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def status_btnStart_handler(self):
        self.ui_status.start()

    def status_btnStop_handler(self):
        self.ui_status.stop()

    #####################
    # invoices handlers #
    #####################
    def invoices_handler(self):
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    #####################
    # updateWP handlers #
    #####################
    def updateWP_handler(self):
        current_tab = self.ui_updateWP.tabs.currentIndex()
        self.updateWP_tabs_handler(current_tab)
        self.ui.contents.showTab(self.ui.contents.UPDATE_WP)

    def updateWP_tabs_handler(self, index):
        if index == self.ui_updateWP.CATEGORIES:
            self.updateWP_init_registered_categories()
        elif index == self.ui_updateWP.PRODUCTS:
            self.updateWP_init_registered_products()

    def updateWP_init_registered_categories(self):
        # dummy data
        categories = []
        for i in range(5):
            random_int = random.randint(1, 10000)
            category = [
                random_int,
                f'Category{random_int}',
                random_int * 2,
                datetime.now().strftime('%Y/%m/%d')
            ]
            categories.append(category)
        self.ui_updateWP.registeredCategoryTable.setRecords(categories)

    def updateWP_init_registered_products(self):
        # dummy data
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
        self.ui_updateWP.registeredProductsTable.setRecords(products)

    def updateWP_action_dispatcher(self, tab, action):
        if tab == self.ui_updateWP.CATEGORIES:
            if action == self.ui_updateWP.ADD:
                self.updateWP_add_category()
            elif action == self.ui_updateWP.EDIT:
                self.updateWP_edit_category()
            elif action == self.ui_updateWP.REMOVE:
                self.updateWP_remove_category()
            elif action == self.ui_updateWP.UPDATE:
                self.updateWP_update_categories()
        elif tab == self.ui_updateWP.PRODUCTS:
            if action == self.ui_updateWP.ADD:
                self.updateWP_add_product()
            elif action == self.ui_updateWP.EDIT:
                self.updateWP_edit_product()
            elif action == self.ui_updateWP.REMOVE:
                self.updateWP_remove_product()
            elif action == self.ui_updateWP.UPDATE:
                self.updateWP_update_products()

    def updateWP_add_category(self):
        new_category = [
            random.randint(1, 10000),
            f'Category{random.randint(1, 10000)}',
            random.randint(1, 10000),
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.ui_updateWP.registeredCategoryTable.addRecord(new_category)
        msg_txt = 'New Category Registered Successfully.'
        msg = Message(self.ui_updateWP, Message.SUCCESS, msg_txt)
        msg.show()

    def updateWP_edit_category(self):
        category_index = self.ui_updateWP.registeredCategoryTable.getCurrentRecordIndex()
        if category_index is not None:
            category = self.ui_updateWP.registeredCategoryTable.getRecord(category_index)
            category[1] = category[1] + '-edited'
            self.ui_updateWP.registeredCategoryTable.updateRecord(category_index, category)
            msg = Message(self.ui_updateWP, Message.SUCCESS, 'Category Updated Successfully.')
            msg.show()

    def updateWP_remove_category(self):
        category_index = self.ui_updateWP.registeredCategoryTable.getCurrentRecordIndex()
        if category_index is not None:
            self.ui_updateWP.registeredCategoryTable.removeRecord(category_index)
            msg = Message(self.ui_updateWP, Message.SUCCESS, 'Category Removed Successfully.')
            msg.show()

    def updateWP_update_categories(self):
        print('update categories on wordpress')

    def updateWP_add_product(self):
        new_product = [
            random.randint(1, 10000),
            random.randint(1, 10000),
            f'Product{random.randint(1, 10000)}',
            random.randint(1, 10000),
            datetime.now().strftime('%Y/%m/%d')
        ]
        self.ui_updateWP.registeredProductsTable.addRecord(new_product)
        msg_txt = 'New Product Registered Successfully.'
        msg = Message(self.ui_updateWP, Message.SUCCESS, msg_txt)
        msg.show()

    def updateWP_edit_product(self):
        product_index = self.ui_updateWP.registeredProductsTable.getCurrentRecordIndex()
        if product_index is not None:
            product = self.ui_updateWP.registeredProductsTable.getRecord(product_index)
            product[2] = product[2] + '-edited'
            self.ui_updateWP.registeredProductsTable.updateRecord(product_index, product)
            msg = Message(self.ui_updateWP, Message.SUCCESS, 'Product Updated Successfully.')
            msg.show()

    def updateWP_remove_product(self):
        product_index = self.ui_updateWP.registeredProductsTable.getCurrentRecordIndex()
        if product_index is not None:
            self.ui_updateWP.registeredProductsTable.removeRecord(product_index)
            msg = Message(self.ui_updateWP, Message.SUCCESS, 'Product Removed Successfully.')
            msg.show()

    def updateWP_update_products(self):
        print('update products on wordpress')

    #####################
    # settings handlers #
    #####################
    def settings_handler(self):
        self.ui_settings.set({
            'wc': s.get('wc', {}),
            'moein': s.get('moein', {})
        })
        self.ui.contents.showTab(self.ui.contents.SETTINGS)

    def settings_btnSave_handler(self):
        try:
            settings = self.ui_settings.get()
            s.set('wc', settings.get('wc'))
            s.set('moein', settings.get('moein'))
            s.save()
        except Exception as e:
            lvl = Message.ERROR
            msg_txt = 'Cannot Save Settings'
            details = str(e)
        else:
            lvl = Message.SUCCESS
            msg_txt = 'Settings Saved Successfully.'
            details = None
        msg = Message(self.ui_settings, lvl, msg_txt, details)
        msg.show()

    def settings_btnClear_handler(self):
        self.ui_settings.clear()

    #################
    # logs handlers #
    #################
    def logs_handler(self):
        self.ui.contents.showTab(self.ui.contents.LOGS)

    #################
    # help handlers #
    #################
    def help_handler(self):
        self.ui.contents.showTab(self.ui.contents.HELP)

    ##################
    # about handlers #
    ##################
    def about_handler(self):
        self.ui.contents.showTab(self.ui.contents.ABOUT)
