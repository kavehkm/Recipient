# pyqt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLabel, QPushButton, QLineEdit,
                             QComboBox, QTabWidget, QTableWidget, QTableWidgetItem)


class BaseTab(QWidget):
    """Base Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupTab()
        self.setStyles()
        self.connectSignals()

    def setupTab(self):
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        self.generalLayout.setContentsMargins(0, 0, 0, 0)

    def setStyles(self):
        pass

    def connectSignals(self):
        pass


class StatusTab(BaseTab):
    """Status Tab"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # default state: stopped
        self.stop()

    def setupTab(self):
        super().setupTab()
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
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Invoices Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class UpdateWPTab(BaseTab):
    """Update WP Tab"""
    # tabs
    PRODUCTS = 0
    CATEGORIES = 1
    # controls
    ADD = 0
    EDIT = 1
    REMOVE = 2
    UPDATE = 3
    # signals
    signalAction = pyqtSignal(int, int)

    def setupTab(self):
        super().setupTab()
        # tabs
        self.tabs = QTabWidget()
        self.generalLayout.addWidget(self.tabs)
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
        # tabs contents
        self.setupRegisteredProducts()
        self.setupRegisteredCategories()

    def setupRegisteredProducts(self):
        self.tabs.addTab(QTableWidget(), 'Products')

    def setupRegisteredCategories(self):
        self.tabs.addTab(QTableWidget(), 'Categories')

    def setStyles(self):
        self.setStyleSheet("""
            QTabBar::tab{
                min-height: 10ex;
                min-width: 30ex;
            }
            QTableWidget{
                border: none;
            }
            QPushButton{
                height: 25px;
                width: 80px;
            }
        """)

    def connectSignals(self):
        self.btnAdd.clicked.connect(self._btnAddHandler)
        self.btnEdit.clicked.connect(self._btnEditHandler)
        self.btnRemove.clicked.connect(self._btnRemoveHandler)
        self.btnUpdateWP.clicked.connect(self._btnUpdateWPHandler)

    def _btnAddHandler(self):
        self.signalAction.emit(self.tabs.currentIndex(), self.ADD)

    def _btnEditHandler(self):
        self.signalAction.emit(self.tabs.currentIndex(), self.EDIT)

    def _btnRemoveHandler(self):
        self.signalAction.emit(self.tabs.currentIndex(), self.REMOVE)

    def _btnUpdateWPHandler(self):
        self.signalAction.emit(self.tabs.currentIndex(), self.UPDATE)


class SettingsTab(BaseTab):
    """Settings Tab"""
    def setupTab(self):
        super().setupTab()
        # settings frame
        self.settingsFrame = QFrame()
        self.settingsFrame.setObjectName('SettingsFrame')
        self.generalLayout.addWidget(self.settingsFrame)
        # settings layout
        self.settingsLayout = QVBoxLayout()
        self.settingsFrame.setLayout(self.settingsLayout)
        # form
        self.form = QFormLayout()
        self.form.setVerticalSpacing(8)
        self.settingsLayout.addLayout(self.form)
        # woocommerce settings
        # header
        wcHeader = QLabel('<h3>WooCommerce API</h3>')
        wcHeader.setFixedHeight(60)
        self.form.addRow(wcHeader)
        # url
        self.urlLabel = QLabel('URL')
        self.url = QLineEdit()
        self.form.addRow(self.urlLabel, self.url)
        # consumer key
        self.ckeyLabel = QLabel('Consumer Key')
        self.ckey = QLineEdit()
        self.form.addRow(self.ckeyLabel, self.ckey)
        # secret key
        self.skeyLabel = QLabel('Secret Key')
        self.skey = QLineEdit()
        self.form.addRow(self.skeyLabel, self.skey)
        # version
        self.versionLabel = QLabel('Version')
        self.version = QComboBox()
        self.version.setFixedWidth(200)
        self.version.addItems(['wc/v3', 'wc/v2', 'wc/v1'])
        self.form.addRow(self.versionLabel, self.version)
        # moein db settings
        # header
        moeinHeader = QLabel('<h3>Moein DB</h3>')
        moeinHeader.setFixedHeight(60)
        self.form.addRow(moeinHeader)
        # server
        self.serverLabel = QLabel('Server')
        self.server = QLineEdit()
        self.form.addRow(self.serverLabel, self.server)
        # username
        self.usernameLabel = QLabel('Username')
        self.username = QLineEdit()
        self.form.addRow(self.usernameLabel, self.username)
        # password
        self.passwordLabel = QLabel('Password')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.form.addRow(self.passwordLabel, self.password)
        # database
        self.databaseLabel = QLabel('DataBase')
        self.database = QLineEdit()
        self.form.addRow(self.databaseLabel, self.database)
        # form buttons
        btnLayout = QHBoxLayout()
        self.btnClear = QPushButton('Clear')
        self.btnSave = QPushButton('Save')
        btnLayout.addStretch(1)
        btnLayout.addWidget(self.btnSave)
        btnLayout.addWidget(self.btnClear)
        self.form.addRow(QLabel(), btnLayout)
        # add stretch at the end
        self.generalLayout.addStretch(1)

    def setStyles(self):
        self.setStyleSheet("""
            #SettingsFrame{
                border: 1px solid silver;
            }
            QLabel{
                margin-right: 50px;
            }
            QPushButton{
                height: 30px;
                width: 80px;
                margin-left: 5px;
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
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Logs Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class HelpTab(BaseTab):
    """Help Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>Help Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class AboutTab(BaseTab):
    """About Tab"""
    def setupTab(self):
        super().setupTab()
        self.lbl = QLabel()
        self.lbl.setText('<h3>About Tab</h3>')
        self.generalLayout.addWidget(self.lbl)


class ContentsWidget(QWidget):
    """Contents Widget"""
    STATUS =    0
    INVOICES =  1
    UPDATE_WP = 2
    SETTINGS =  3
    LOGS =      4
    HELP =      5
    ABOUT =     6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.setupContents()

    def setupContents(self):
        # set general layout
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)
        """
        attach tabs
        """
        # status
        self.status = StatusTab()
        # invoices
        self.invoices = InvoicesTab()
        # update_wp
        self.updateWP = UpdateWPTab()
        # settings
        self.settings = SettingsTab()
        # logs
        self.logs = LogsTab()
        # help
        self.help = HelpTab()
        # about
        self.about = AboutTab()
        """
        register tabs
        """
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
        """
        set default tab
        """
        self.showTab(self.STATUS)

    def showTab(self, tabId):
        for tab in self.tabs:
            tab.hide()
        self.tabs[tabId].show()
