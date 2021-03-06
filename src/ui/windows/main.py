# internal
# noinspection PyUnresolvedReferences
from src.ui.resources import icons
from src.translation import _
from .order_details import OrderDetails
from src.ui.components import (BaseWidget, Table, Tab, ScrollArea, GpBox, SMEdit, SMDateTimeEdit, SMCombo, SMSpin,
                               MainMenuButton, AddMDButton, EditMDButton, DeleteMDButton, SyncMDButton, SaveMDButton,
                               SaveAllMDButton, RefreshMDButton, ClearMDButton, StartMDButton, StopMDButton)


# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFrame, QHBoxLayout,
                             QVBoxLayout, QFormLayout, QLabel, QCheckBox, QRadioButton)


########
# Menu #
########
class Menu(BaseWidget):
    """Menu"""
    def __init__(self, parent=None):
        self.buttons = []
        self.main = parent
        super().__init__(parent)

    def setupLayout(self):
        super().setupLayout()
        self.setFixedWidth(200)

    def setupWidget(self):
        # setup buttons
        # - status
        self.btnStatus = MainMenuButton(_('Status'))
        self.btnStatus.setIcon(QIcon(':/icons/btnStatus.png'))
        # - invoices
        self.btnInvoices = MainMenuButton(_('Invoices'))
        self.btnInvoices.setIcon(QIcon(':/icons/btnInvoices.png'))
        # - woocommerce
        self.btnWooCommerce = MainMenuButton(_('WooCommerce'))
        self.btnWooCommerce.setIcon(QIcon(':/icons/btnWooCommerce.png'))
        # - settings
        self.btnSettings = MainMenuButton(_('Settings'))
        self.btnSettings.setIcon(QIcon(':/icons/btnSettings.png'))
        # - logs
        self.btnLogs = MainMenuButton(_('Logs'))
        self.btnLogs.setIcon(QIcon(':/icons/btnLogs.png'))
        # - help
        self.btnHelp = MainMenuButton(_('Help'))
        self.btnHelp.setIcon(QIcon(':/icons/btnHelp.png'))
        # - about
        self.btnAbout = MainMenuButton(_('About'))
        self.btnAbout.setIcon(QIcon(':/icons/btnAbout.png'))
        # register buttons
        self.buttons = [
            self.btnStatus,
            self.btnInvoices,
            self.btnWooCommerce,
            self.btnSettings,
            self.btnLogs,
            self.btnHelp,
            self.btnAbout
        ]
        for btn in self.buttons:
            btn.setIconSize(QSize(24, 24))
            self.generalLayout.addWidget(btn)
        # add stretch at the end
        self.generalLayout.addStretch(1)

    def setFoucus(self, index):
        for btn in self.buttons:
            btn.setDefault(False)
        self.buttons[index].setDefault(True)


############
# Contents #
############
class BaseTab(BaseWidget):
    """Base Tab"""
    def setupLayout(self):
        super().setupLayout()
        self.generalLayout.setContentsMargins(0, 0, 0, 0)


class StatusTab(BaseTab):
    """Status Tab"""
    def bootstrap(self):
        super().bootstrap()
        # default state
        self.stop()

    def setupWidget(self):
        # service frame
        self.serviceFrame = QFrame()
        self.serviceFrame.setObjectName('ServiceFrame')
        self.generalLayout.addWidget(self.serviceFrame)
        # service layout
        self.serviceLayout = QVBoxLayout()
        self.serviceFrame.setLayout(self.serviceLayout)
        # service name
        self.serviceName = QLabel('<h3>{}</h3>'.format(_('Recipient Engine')))
        self.serviceName.setFixedHeight(60)
        self.serviceLayout.addWidget(self.serviceName)
        # service state
        serviceStateLayout = QHBoxLayout()
        serviceStateLayout.setContentsMargins(0, 10, 0, 10)
        self.serviceStateVal = QLabel()
        serviceStateLayout.addWidget(self.serviceStateVal)
        self.serviceLayout.addLayout(serviceStateLayout)
        # service control
        serviceControlLayout = QHBoxLayout()
        self.btnStart = StartMDButton(_('Start'))
        self.btnStop = StopMDButton(_('Stop'))
        serviceControlLayout.addWidget(self.btnStart)
        serviceControlLayout.addWidget(self.btnStop)
        serviceControlLayout.addStretch(1)
        self.serviceLayout.addLayout(serviceControlLayout)
        # add stretch at the end
        self.generalLayout.addStretch(1)

    def setStyles(self):
        self.setStyleSheet("""
            #ServiceFrame{
                border: 1px solid silver;
                border-right-width: 2px;
            }
            #ServiceFrame[state="start"]{
                border-right-color: #26d926;
            }
            #ServiceFrame[state="stop"]{
                border-right-color: red;
            }
            #ServiceFrame[state="connecting"]{
                border-right-color: orange;
            }
        """)

    def start(self):
        self.serviceStateVal.setText(_('running'))
        self.btnStart.setDisabled(True)
        self.btnStop.setEnabled(True)
        self.serviceFrame.setProperty('state', 'start')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def stop(self):
        self.serviceStateVal.setText(_('stopped'))
        self.btnStart.setEnabled(True)
        self.btnStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'stop')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def connecting(self):
        self.serviceStateVal.setText(_('connecting'))
        self.btnStart.setDisabled(True)
        self.btnStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'connecting')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def connecting_count(self, counter):
        self.serviceStateVal.setText(_('Connecting after {} seconds...').format(counter))


class InvoicesTab(BaseTab):
    """Invoices Tab"""
    # tabs
    ORDERS = 0
    INVOICES = 1

    def setupWidget(self):
        # tabs
        self.tabs = Tab()
        self.generalLayout.addWidget(self.tabs)
        # - orders
        self.ordersTable = Table([_('ID'), _('Order'), _('Date'), _('Status'), _('Total')], [1, 3, 2, 1, 1])
        self.tabs.addTab(self.ordersTable, _('Orders'))
        # - invoices
        self.invoicesTable = Table([_('ID'), _('Customer'), _('OrderID'), _('SavedDate')], [1, 3, 1, 2])
        self.tabs.addTab(self.invoicesTable, _('Invoices'))
        # controls
        self.controlLayout = QHBoxLayout()
        self.controlLayout.addStretch(1)
        self.generalLayout.addLayout(self.controlLayout)
        self.btnRefresh = RefreshMDButton(_('Refresh'))
        self.btnSaveAll = SaveAllMDButton(_('Save all'))
        self.btnRemove = DeleteMDButton(_('Remove'))
        self.btnRemove.setHidden(True)
        self.controlLayout.addWidget(self.btnRefresh)
        self.controlLayout.addWidget(self.btnSaveAll)
        self.controlLayout.addWidget(self.btnRemove)

        # attach order details dialog
        self.orderDetails = OrderDetails(self)

    def connectSignals(self):
        self.tabs.currentChanged.connect(self.tabHandler)

    def tabHandler(self, index):
        if index == self.ORDERS:
            self.btnRemove.setHidden(True)
            self.btnRefresh.setHidden(False)
            self.btnSaveAll.setHidden(False)
        else:
            self.btnRemove.setHidden(False)
            self.btnRefresh.setHidden(True)
            self.btnSaveAll.setHidden(True)


class WooCommerceTab(BaseTab):
    """WooCommerce Tab"""
    # tabs
    PRODUCTS = 0
    CATEGORIES = 1

    def setupWidget(self):
        # tabs
        self.tabs = Tab()
        self.generalLayout.addWidget(self.tabs)
        _sizes = [1, 3, 1, 2]
        # - products
        self.productsTable = Table([_('ID'), _('Name'), _('WCID'), _('LastUpdate')], _sizes)
        self.tabs.addTab(self.productsTable, _('Products'))
        # - categories
        self.categoriesTable = Table([_('ID'), _('Name'), _('WCID'), _('LastUpdate')], _sizes)
        self.tabs.addTab(self.categoriesTable, _('Categories'))
        # controls
        controlLayout = QHBoxLayout()
        controlLayout.addStretch(1)
        self.btnAdd = AddMDButton(_('Add'))
        self.btnEdit = EditMDButton(_('Edit'))
        self.btnRemove = DeleteMDButton(_('Remove'))
        self.btnUpdate = SyncMDButton(_('Update'))
        controlLayout.addWidget(self.btnAdd)
        controlLayout.addWidget(self.btnEdit)
        controlLayout.addWidget(self.btnRemove)
        controlLayout.addWidget(self.btnUpdate)
        self.generalLayout.addLayout(controlLayout)


class SettingsTab(BaseTab):
    """Settings Tab"""
    def setupWidget(self):
        # scrollable area
        self.scrollableArea = ScrollArea()
        self.generalLayout.addWidget(self.scrollableArea)
        # settings layout
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setSpacing(20)
        self.scrollableArea.setLayout(self.settingsLayout)
        # general settings
        self.general = GpBox(' {} '.format(_('General')))
        self.settingsLayout.addWidget(self.general)
        self.generalForm = QFormLayout()
        self.general.setLayout(self.generalForm)
        # - language
        self.language = SMCombo()
        self.language.addItems(['English', 'Persian'])
        self.generalForm.addRow(QLabel(_('Language')), self.language)
        # moein settings
        self.moein = GpBox(' {} '.format(_('Moein')))
        self.settingsLayout.addWidget(self.moein)
        self.moeinForm = QFormLayout()
        self.moein.setLayout(self.moeinForm)
        # - server
        self.server = SMEdit()
        self.moeinForm.addRow(QLabel(_('Server')), self.server)
        # - username
        self.username = SMEdit()
        self.moeinForm.addRow(QLabel(_('Username')), self.username)
        # - password
        self.password = SMEdit(password=True)
        self.moeinForm.addRow(QLabel(_('Password')), self.password)
        # - database
        self.database = SMEdit()
        self.moeinForm.addRow(QLabel(_('Database')), self.database)
        # woocommerce settings
        self.woocommerce = GpBox(' {} '.format(_('WooCommerce')))
        self.settingsLayout.addWidget(self.woocommerce)
        self.woocommerceForm = QFormLayout()
        self.woocommerce.setLayout(self.woocommerceForm)
        # - url
        self.url = SMEdit()
        self.woocommerceForm.addRow(QLabel(_('URL')), self.url)
        # - consumer key
        self.ckey = SMEdit()
        self.woocommerceForm.addRow(QLabel(_('Consumer key')), self.ckey)
        # - secret key
        self.skey = SMEdit()
        self.woocommerceForm.addRow(QLabel(_('Secret key')), self.skey)
        # - version
        self.version = SMCombo()
        self.version.addItems(['wc/v3', 'wc/v2', 'wc/v1'])
        self.woocommerceForm.addRow(QLabel(_('Version')), self.version)
        # - timeout
        self.timeout = SMSpin()
        self.woocommerceForm.addRow(QLabel(_('Timeout')), self.timeout)
        # import/export settings
        self.importExport = GpBox(' {} '.format(_('Import/Export')))
        self.settingsLayout.addWidget(self.importExport)
        self.importExportForm = QFormLayout()
        self.importExport.setLayout(self.importExportForm)
        # - sku hint
        self.skuHint = QCheckBox(_('SKU'))
        self.importExportForm.addRow(QLabel(_('Hints')), self.skuHint)
        # orders settings
        self.orders = GpBox(' {} '.format(_('Orders')))
        self.settingsLayout.addWidget(self.orders)
        self.ordersForm = QFormLayout()
        self.orders.setLayout(self.ordersForm)
        # - status
        # -- options
        self.cbxPending = QCheckBox(_('Pending'))
        self.cbxProcessing = QCheckBox(_('Processing'))
        self.cbxOnHold = QCheckBox(_('On Hold'))
        self.cbxCompleted = QCheckBox(_('Completed'))
        self.cbxCancelled = QCheckBox(_('Cancelled'))
        self.cbxRefunded = QCheckBox(_('Refunded'))
        self.cbxFailed = QCheckBox(_('Failed'))
        self.cbxTrash = QCheckBox(_('Trash'))
        self.cbxAny = QCheckBox(_('Any'))
        self.statusOptions = {
            'pending': self.cbxPending,
            'processing': self.cbxProcessing,
            'on-hold': self.cbxOnHold,
            'completed': self.cbxCompleted,
            'cancelled': self.cbxCancelled,
            'refunded': self.cbxRefunded,
            'failed': self.cbxFailed,
            'trash': self.cbxTrash,
            'any': self.cbxAny
        }
        # -- options layout
        statusOptionsLayout = QVBoxLayout()
        statusOptions1Layout = QHBoxLayout()
        statusOptions2Layout = QHBoxLayout()
        statusOptions3Layout = QHBoxLayout()
        statusOptionsLayout.addLayout(statusOptions1Layout)
        statusOptionsLayout.addLayout(statusOptions2Layout)
        statusOptionsLayout.addLayout(statusOptions3Layout)
        statusOptionsLayout.addSpacing(5)
        # any as gp1
        statusOptions1Layout.addWidget(self.cbxAny)
        # pending, processing, on-hold and complete as gp 2
        statusOptions2Layout.addWidget(self.cbxPending)
        statusOptions2Layout.addWidget(self.cbxProcessing)
        statusOptions2Layout.addWidget(self.cbxOnHold)
        statusOptions2Layout.addWidget(self.cbxCompleted)
        # cancelled, refunded, failed and trash as gp3
        statusOptions3Layout.addWidget(self.cbxCancelled)
        statusOptions3Layout.addWidget(self.cbxRefunded)
        statusOptions3Layout.addWidget(self.cbxFailed)
        statusOptions3Layout.addWidget(self.cbxTrash)
        self.ordersForm.addRow(QLabel(_('Status')), statusOptionsLayout)
        # - after
        self.after = SMDateTimeEdit()
        self.ordersForm.addRow(QLabel(_('After')), self.after)
        # - before
        self.before = SMDateTimeEdit()
        self.ordersForm.addRow(QLabel(_('Before')), self.before)
        # invoice settings
        self.invoices = GpBox(' {} '.format(_('Invoices')))
        self.settingsLayout.addWidget(self.invoices)
        self.invoicesForm = QFormLayout()
        self.invoices.setLayout(self.invoicesForm)
        # - guest
        self.guest = SMSpin()
        self.invoicesForm.addRow(QLabel(_('Guest customer')), self.guest)
        # - repository
        self.repository = SMSpin()
        self.invoicesForm.addRow(QLabel(_('Products repository')), self.repository)
        # - price level
        self.priceLevel = SMSpin()
        self.invoicesForm.addRow(QLabel(_('Products price-level')), self.priceLevel)
        # - type
        self.type = SMSpin()
        self.invoicesForm.addRow(QLabel(_('Invoice type')), self.type)
        # engine settings
        self.engine = GpBox(' {} '.format(_('Updater Engine')))
        self.settingsLayout.addWidget(self.engine)
        self.engineForm = QFormLayout()
        self.engine.setLayout(self.engineForm)
        # - start
        startOptionsLayout = QHBoxLayout()
        self.autoStart = QRadioButton(_('Auto'))
        self.manualStart = QRadioButton(_('Manual'))
        self.manualStart.setChecked(True)
        startOptionsLayout.addWidget(self.autoStart)
        startOptionsLayout.addWidget(self.manualStart)
        self.engineForm.addRow(QLabel(_('Start type')), startOptionsLayout)
        # - tasks
        tasksOptionsLayout = QHBoxLayout()
        self.wcUpdate = QCheckBox(_('Update woocommerce'))
        self.convertOrders = QCheckBox(_('Convert orders'))
        tasksOptionsLayout.addWidget(self.wcUpdate)
        tasksOptionsLayout.addWidget(self.convertOrders)
        self.engineForm.addRow(QLabel(_('Tasks')), tasksOptionsLayout)
        # - interval
        self.engineInterval = SMSpin()
        self.engineForm.addRow(QLabel(_('Interval')), self.engineInterval)
        # add stretch at end
        self.settingsLayout.addStretch(1)
        # controls
        controlLayout = QHBoxLayout()
        controlLayout.addStretch(1)
        self.btnClear = ClearMDButton(_('Clear'))
        self.btnSave = SaveMDButton(_('Save'))
        controlLayout.addWidget(self.btnClear)
        controlLayout.addWidget(self.btnSave)
        self.generalLayout.addLayout(controlLayout)

    def setStyles(self):
        self.setStyleSheet("""
            QLabel{
                height: 20px;
                margin-right: 50px;
            }
        """)

    def get(self):
        return {
            'general': {
                'language': self.language.currentText()
            },
            'wc': {
                'url': self.url.text(),
                'ckey': self.ckey.text(),
                'skey': self.skey.text(),
                'version': self.version.currentText(),
                'timeout': self.timeout.value()
            },
            'moein': {
                'server': self.server.text(),
                'username': self.username.text(),
                'password': self.password.text(),
                'database': self.database.text()
            },
            'import_export': {
                'sku_hint': self.skuHint.isChecked()
            },
            'orders': {
                'status': [option for option, cbx in self.statusOptions.items() if cbx.isChecked()],
                'after': self.after.getDateTime(),
                'before': self.before.getDateTime()
            },
            'invoices': {
                'guest': self.guest.value(),
                'repository': self.repository.value(),
                'price_level': self.priceLevel.value(),
                'type': self.type.value()
            },
            'engine': {
                'auto_start': self.autoStart.isChecked(),
                'wc_update': self.wcUpdate.isChecked(),
                'convert_orders': self.convertOrders.isChecked(),
                'interval': self.engineInterval.value()
            }
        }

    def set(self, settings):
        # general
        general = settings['general']
        self.language.setCurrentText(general['language'])
        # woocommerce
        wc = settings['wc']
        self.url.setText(wc['url']),
        self.ckey.setText(wc['ckey'])
        self.skey.setText(wc['skey'])
        self.version.setCurrentText(wc['version'])
        self.timeout.setValue(wc['timeout'])
        # moein
        moein = settings['moein']
        self.server.setText(moein['server'])
        self.username.setText(moein['username'])
        self.password.setText(moein['password'])
        self.database.setText(moein['database'])
        # import/export
        import_export = settings['import_export']
        self.skuHint.setChecked(import_export['sku_hint'])
        # orders
        orders = settings['orders']
        for option in orders['status']:
            self.statusOptions[option].setChecked(True)
        self.after.setDateTime(orders['after'])
        self.before.setDateTime(orders['before'])
        # invoices
        invoices = settings['invoices']
        self.guest.setValue(invoices['guest'])
        self.repository.setValue(invoices['repository'])
        self.priceLevel.setValue(invoices['price_level'])
        self.type.setValue(invoices['type'])
        # engine
        engine = settings['engine']
        self.autoStart.setChecked(engine['auto_start'])
        self.wcUpdate.setChecked(engine['wc_update'])
        self.convertOrders.setChecked(engine['convert_orders'])
        self.engineInterval.setValue(engine['interval'])

    def clear(self):
        # woocommerce
        self.url.clear()
        self.ckey.clear()
        self.skey.clear()
        # moein
        self.server.clear()
        self.username.clear()
        self.password.clear()
        self.database.clear()


class LogsTab(BaseTab):
    """Logs Tab"""
    def setupWidget(self):
        pass


class HelpTab(BaseTab):
    """Help Tab"""
    def setupWidget(self):
        pass


class AboutTab(BaseTab):
    """About Tab"""
    def setupWidget(self):
        pass


class Contents(BaseWidget):
    """Contents"""
    STATUS =        0
    INVOICES =      1
    WOOCOMMERCE =   2
    SETTINGS =      3
    LOGS =          4
    HELP =          5
    ABOUT =         6

    def __init__(self, parent=None):
        self.tabs = []
        self.main = parent
        super().__init__(parent)

    def bootstrap(self):
        super().bootstrap()
        # default tab
        self.showTab(self.STATUS)

    def setupWidget(self):
        # attach tabs
        # - status
        self.status = StatusTab()
        # - invoices
        self.invoices = InvoicesTab()
        # - woocommerce
        self.woocommerce = WooCommerceTab()
        # - settings
        self.settings = SettingsTab()
        # - logs
        self.logs = LogsTab()
        # - help
        self.help = HelpTab()
        # - about
        self.about = AboutTab()
        # register tabs
        self.tabs = [
            self.status,
            self.invoices,
            self.woocommerce,
            self.settings,
            self.logs,
            self.help,
            self.about
        ]
        for tab in self.tabs:
            self.generalLayout.addWidget(tab)

    def showTab(self, tabId):
        # show current tab
        for tab in self.tabs:
            tab.hide()
        self.tabs[tabId].show()
        # set focus on current menu button
        self.main.menu.setFoucus(tabId)


###############
# Main Window #
###############
class Main(QMainWindow):
    """Main Window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bootstrap()

    def bootstrap(self):
        self.setupLayout()
        self.setupMain()

    def setupLayout(self):
        # central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # general layout
        self.generalLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.generalLayout)
        # set windows title
        self.setWindowTitle(_('Recipient'))
        # set windows geometry
        self.setGeometry(100, 100, 809, 500)
        # set window min-size
        self.setMinimumSize(809, 500)
        # set window icon
        windowIcon = QIcon()
        sizes = [16, 24, 32, 48, 96, 256]
        for size in sizes:
            iconFile = ':/icons/windowIcon{}.png'.format(size)
            windowIcon.addFile(iconFile, QSize(size, size))
        self.setWindowIcon(windowIcon)

    def setupMain(self):
        self.menu = Menu(self)
        self.generalLayout.addWidget(self.menu)
        self.contents = Contents(self)
        self.generalLayout.addWidget(self.contents)
