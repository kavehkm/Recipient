# internal
from src import settings as s


class Controller(object):
    """Controller"""
    def __init__(self, ui):
        self.ui = ui
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
        self.ui.contents.status.btnStart.clicked.connect(self.status_btnStart_handler)
        self.ui.contents.status.btnStop.clicked.connect(self.status_btnStop_handler)
        # contents: settings tab
        self.ui.contents.settings.btnSave.clicked.connect(self.settings_btnSave_handler)
        self.ui.contents.settings.btnClear.clicked.connect(self.settings_btnClear_handler)
        # contents: updateWP tab
        self.ui.contents.updateWP.tabs.currentChanged.connect(self.updateWP_tabs_handler)
        self.ui.contents.updateWP.signalAction.connect(self.updateWP_action_dispatcher)

    ###################
    # status handlers #
    ###################
    def status_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def status_btnStart_handler(self):
        self.ui.contents.status.start()

    def status_btnStop_handler(self):
        self.ui.contents.status.stop()

    #####################
    # invoices handlers #
    #####################
    def invoices_handler(self):
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    #####################
    # updateWP handlers #
    #####################
    def updateWP_handler(self):
        current_tab = self.ui.contents.updateWP.tabs.currentIndex()
        self.updateWP_tabs_handler(current_tab)
        self.ui.contents.showTab(self.ui.contents.UPDATE_WP)

    def updateWP_tabs_handler(self, index):
        print(index)

    def updateWP_action_dispatcher(self, tab, action):
        # create alias
        update_wp = self.ui.contents.updateWP
        if tab == update_wp.CATEGORIES:
            if action == update_wp.ADD:
                self.updateWP_add_category()
            elif action == update_wp.EDIT:
                self.updateWP_edit_category()
            elif action == update_wp.REMOVE:
                self.updateWP_remove_category()
            elif action == update_wp.UPDATE:
                self.updateWP_update_categories()
        elif tab == update_wp.PRODUCTS:
            if action == update_wp.ADD:
                self.updateWP_add_product()
            elif action == update_wp.EDIT:
                self.updateWP_edit_product()
            elif action == update_wp.REMOVE:
                self.updateWP_remove_product()
            elif action == update_wp.UPDATE:
                self.updateWP_update_products()

    def updateWP_add_category(self):
        print('add new category')

    def updateWP_edit_category(self):
        print('edit category')

    def updateWP_remove_category(self):
        print('remove category')

    def updateWP_update_categories(self):
        print('update categories on wordpress')

    def updateWP_add_product(self):
        print('add new product')

    def updateWP_edit_product(self):
        print('edit product')

    def updateWP_remove_product(self):
        print('remove product')

    def updateWP_update_products(self):
        print('update products on wordpress')

    #####################
    # settings handlers #
    #####################
    def settings_handler(self):
        self.ui.contents.settings.set({
            'wc': s.get('wc', {}),
            'moein': s.get('moein', {})
        })
        self.ui.contents.showTab(self.ui.contents.SETTINGS)

    def settings_btnSave_handler(self):
        settings = self.ui.contents.settings.get()
        s.set('wc', settings.get('wc'))
        s.set('moein', settings.get('moein'))
        s.save()

    def settings_btnClear_handler(self):
        self.ui.contents.settings.clear()

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
