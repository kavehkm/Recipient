# internal
from src.ui.resources import icons
from src.ui.components import BaseWidget, Table
# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFrame, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QFormLayout,
                             QPushButton, QLabel, QLineEdit, QComboBox)


########
# Menu #
########
class Menu(BaseWidget):
    """Menu"""
    def setupWidget(self):
        # setup buttons
        # - status
        self.btnStatus = QPushButton('Status')
        self.btnStatus.setIcon(QIcon(':/icons/btnStatus.png'))
        # - invoices
        self.btnInvoices = QPushButton('Invoices')
        self.btnInvoices.setIcon(QIcon(':/icons/btnInvoices.png'))
        # - update wp
        self.btnUpdateWP = QPushButton('Update WP')
        self.btnUpdateWP.setIcon(QIcon(':/icons/btnUpdateWP.png'))
        # - settings
        self.btnSettings = QPushButton('Settings')
        self.btnSettings.setIcon(QIcon(':/icons/btnSettings.png'))
        # - logs
        self.btnLogs = QPushButton('Logs')
        self.btnLogs.setIcon(QIcon(':/icons/btnLogs.png'))
        # - help
        self.btnHelp = QPushButton('Help')
        self.btnHelp.setIcon(QIcon(':/icons/btnHelp.png'))
        # - about
        self.btnAbout = QPushButton('About')
        self.btnAbout.setIcon(QIcon(':/icons/btnAbout.png'))
        # register buttons
        buttons = [
            self.btnStatus,
            self.btnInvoices,
            self.btnUpdateWP,
            self.btnSettings,
            self.btnLogs,
            self.btnHelp,
            self.btnAbout
        ]
        for btn in buttons:
            btn.setIconSize(QSize(24, 24))
            self.generalLayout.addWidget(btn)
        # add stretch at the end
        self.generalLayout.addStretch(1)

    def setStyles(self):
        self.setStyleSheet("""
            QPushButton {
                height: 50px;
                text-align: left;
                padding-left: 20px
            }
        """)


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
        self.serviceName = QLabel('<h3>Recipient Engine</h3>')
        self.serviceName.setFixedHeight(60)
        self.serviceLayout.addWidget(self.serviceName)
        # service state
        serviceStateLayout = QHBoxLayout()
        serviceStateLayout.setContentsMargins(0, 10, 0, 10)
        self.serviceStateLabel = QLabel('<b>status: </b>')
        self.serviceStateVal = QLabel()
        serviceStateLayout.addWidget(self.serviceStateLabel)
        serviceStateLayout.addWidget(self.serviceStateVal)
        serviceStateLayout.addStretch(1)
        self.serviceLayout.addLayout(serviceStateLayout)
        # service control
        serviceControlLayout = QHBoxLayout()
        self.btnStart = QPushButton('Start')
        self.btnStop = QPushButton('Stop')
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
            QPushButton{
                height: 25px;
            }
        """)

    def start(self):
        self.serviceStateVal.setText('running')
        self.btnStart.setDisabled(True)
        self.btnStop.setEnabled(True)
        self.serviceFrame.setProperty('state', 'start')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def stop(self):
        self.serviceStateVal.setText('stopped')
        self.btnStart.setEnabled(True)
        self.btnStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'stop')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())

    def connecting(self):
        self.serviceStateVal.setText('connecting')
        self.btnStart.setDisabled(True)
        self.btnStop.setDisabled(True)
        self.serviceFrame.setProperty('state', 'connecting')
        self.serviceFrame.setStyleSheet(self.serviceFrame.styleSheet())


class InvoicesTab(BaseTab):
    """Invoices Tab"""
    def setupWidget(self):
        # table
        self.invoicesTable = Table(['ID', 'Order', 'Date', 'Status', 'Total'])
        self.generalLayout.addWidget(self.invoicesTable)
        # controls
        controlLayout = QHBoxLayout()
        controlLayout.addStretch(1)
        self.btnRefresh = QPushButton('Refresh')
        self.btnSaveAll = QPushButton('Save all')
        controlLayout.addWidget(self.btnRefresh)
        controlLayout.addWidget(self.btnSaveAll)
        self.generalLayout.addLayout(controlLayout)

    def setStyles(self):
        self.setStyleSheet("""
            QPushButton{
                height: 25px;
                width: 80px;
            }
        """)


class UpdateWPTab(BaseTab):
    """Update WP Tab"""
    # tabs
    PRODUCTS = 0
    CATEGORIES = 1

    def setupWidget(self):
        # tabs
        self.tabs = QTabWidget()
        self.generalLayout.addWidget(self.tabs)
        # - products
        self.productsTable = Table(['ID', 'Name', 'WPID', 'LastUpdate'])
        self.tabs.addTab(self.productsTable, 'Products')
        # - categories
        self.categoriesTable = Table(['ID', 'Name', 'WPID', 'LastUpdate'])
        self.tabs.addTab(self.categoriesTable, 'Categories')
        # controls
        controlLayout = QHBoxLayout()
        controlLayout.addStretch(1)
        self.btnAdd = QPushButton('Add')
        self.btnEdit = QPushButton('Edit')
        self.btnRemove = QPushButton('Remove')
        self.btnUpdateWP = QPushButton('Update WP')
        controlLayout.addWidget(self.btnAdd)
        controlLayout.addWidget(self.btnEdit)
        controlLayout.addWidget(self.btnRemove)
        controlLayout.addWidget(self.btnUpdateWP)
        self.generalLayout.addLayout(controlLayout)

    def setStyles(self):
        self.setStyleSheet("""
            QTabBar::tab{
                min-height: 10ex;
                min-width: 30ex;
            }
            QPushButton{
                height: 25px;
                width: 80px;
            }
        """)


class SettingsTab(BaseTab):
    """Settings Tab"""
    def setupWidget(self):
        # tabs
        self.tabs = QTabWidget()
        self.generalLayout.addWidget(self.tabs)
        # moein db settings
        self.moeinForm = QFormLayout()
        moeinFormFrame = QFrame()
        moeinFormFrame.setLayout(self.moeinForm)
        self.tabs.addTab(moeinFormFrame, 'Moein')
        # - server
        self.server = QLineEdit()
        self.moeinForm.addRow(QLabel('Server'), self.server,)
        # - username
        self.username = QLineEdit()
        self.moeinForm.addRow(QLabel('Username'), self.username)
        # - password
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.moeinForm.addRow(QLabel('Password'), self.password)
        # - database
        self.database = QLineEdit()
        self.moeinForm.addRow(QLabel('DataBase'), self.database)
        # woocommerce settings
        self.wcForm = QFormLayout()
        wcFormFrame = QFrame()
        wcFormFrame.setLayout(self.wcForm)
        self.tabs.addTab(wcFormFrame, 'WooCommerce')
        # - url
        self.url = QLineEdit()
        self.wcForm.addRow(QLabel('URL'), self.url)
        # - consumer key
        self.ckey = QLineEdit()
        self.wcForm.addRow(QLabel('Consumer Key'), self.ckey)
        # - secret key
        self.skey = QLineEdit()
        self.wcForm.addRow(QLabel('Secret Key'), self.skey)
        # - version
        self.version = QComboBox()
        self.version.addItems(['wc/v3', 'wc/v2', 'wc/v1'])
        self.wcForm.addRow(QLabel('Version'), self.version)
        # controls
        controlLayout = QHBoxLayout()
        controlLayout.addStretch(1)
        self.btnClear = QPushButton('Clear')
        self.btnSave = QPushButton('Save')
        controlLayout.addWidget(self.btnClear)
        controlLayout.addWidget(self.btnSave)
        self.generalLayout.addLayout(controlLayout)

    def setStyles(self):
        self.setStyleSheet("""
            QTabBar::tab{
                min-height: 10ex;
                min-width: 30ex;
            }
            QLabel{
                height: 20px;
                margin-right: 50px;
            }
            QComboBox, QLineEdit{
                height: 20px;
            }
            QPushButton{
                height: 25px;
                width: 80px;
            }
        """)

    def get(self):
        return {
            'wc': {
                'url': self.url.text(),
                'ckey': self.ckey.text(),
                'skey': self.skey.text(),
                'version': self.version.currentText()
            },
            'moein': {
                'server': self.server.text(),
                'username': self.username.text(),
                'password': self.password.text(),
                'database': self.database.text()
            }
        }

    def set(self, settings):
        # woocommerce
        wc = settings.get('wc')
        self.url.setText(wc.get('url')),
        self.ckey.setText(wc.get('ckey'))
        self.skey.setText(wc.get('skey'))
        self.version.setCurrentText(wc.get('version'))
        # moein
        moein = settings.get('moein')
        self.server.setText(moein.get('server'))
        self.username.setText(moein.get('username'))
        self.password.setText(moein.get('password'))
        self.database.setText(moein.get('database'))

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
    STATUS =    0
    INVOICES =  1
    UPDATE_WP = 2
    SETTINGS =  3
    LOGS =      4
    HELP =      5
    ABOUT =     6

    def __init__(self, parent=None):
        self.tabs = []
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
        # - update_wp
        self.updateWP = UpdateWPTab()
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
            self.updateWP,
            self.settings,
            self.logs,
            self.help,
            self.about
        ]
        for tab in self.tabs:
            self.generalLayout.addWidget(tab)

    def showTab(self, tabId):
        for tab in self.tabs:
            tab.hide()
        self.tabs[tabId].show()


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
        self.setWindowTitle('Recipient')
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
        # set menu widget 30%
        self.menu = Menu(self)
        self.generalLayout.addWidget(self.menu, 30)
        # set content widget 70%
        self.contents = Contents(self)
        self.generalLayout.addWidget(self.contents, 70)
