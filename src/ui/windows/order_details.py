# internal
from src.ui.components import BaseDialog, Table
# pyqt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QLabel, QPushButton


class OrderDetails(BaseDialog):
    """Order Details Dialog"""
    def setupLayout(self):
        super().setupLayout()
        # set dialog title
        self.setWindowTitle('Order details')
        # set dialog geometry
        self.setGeometry(200, 200, 900, 562)

    def setupDialog(self):
        # scrollable area
        self.scrollableArea = QScrollArea()
        self.scrollableArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollableArea.setWidgetResizable(True)
        self.dialogLayout.addWidget(self.scrollableArea)
        # widget
        self.widget = QWidget()
        self.scrollableArea.setWidget(self.widget)
        # order layout
        self.orderLayout = QVBoxLayout()
        self.widget.setLayout(self.orderLayout)

        ###########################
        # Section1: Order Details #
        ###########################
        # widget
        self.section1 = QWidget(objectName='Section')
        self.orderLayout.addWidget(self.section1)
        # layout
        self.layout1 = QVBoxLayout()
        self.section1.setLayout(self.layout1)
        # order title
        title = 'Order #{} {} {}'.format(654, 'Firstname', 'Lastname')
        self.orderTitle = QLabel(title, objectName='OrderTitle')
        self.layout1.addWidget(self.orderTitle)
        # order details layout
        self.detailsLayout = QHBoxLayout()
        self.layout1.addLayout(self.detailsLayout)

        # general
        self.general = QVBoxLayout()
        self.detailsLayout.addLayout(self.general)
        # - title
        self.generalTitle = QLabel('General', objectName='SectionTitle')
        self.general.addWidget(self.generalTitle)
        # - date
        self.dateCreated = QLabel('', objectName='DetailValue')
        self.general.addWidget(QLabel('Date created:'))
        self.general.addWidget(self.dateCreated)
        # - status
        self.status = QLabel('', objectName='DetailValue')
        self.general.addWidget(QLabel('Status:'))
        self.general.addWidget(self.status)
        # - customer
        self.customer = QLabel('', objectName='DetailValue')
        self.general.addWidget(QLabel('Customer:'))
        self.general.addWidget(self.customer)
        # add stretch
        self.general.addStretch(1)

        # billing
        self.billing = QVBoxLayout()
        self.billing.setContentsMargins(20, 0, 20, 0)
        self.detailsLayout.addLayout(self.billing)
        # - title
        self.billingTitle = QLabel('Billing', objectName='SectionTitle')
        self.billing.addWidget(self.billingTitle)
        # - first name and last name
        billingFullnameRow = QHBoxLayout()
        self.billing.addLayout(billingFullnameRow)
        billingFirstnameColumn = QVBoxLayout()
        billingLastnameColumn = QVBoxLayout()
        billingFullnameRow.addLayout(billingFirstnameColumn)
        billingFullnameRow.addLayout(billingLastnameColumn)
        # -- first name
        self.billingFirstname = QLabel('', objectName='DetailValue')
        billingFirstnameColumn.addWidget(QLabel('First name'))
        billingFirstnameColumn.addWidget(self.billingFirstname)
        # -- last name
        self.billingLastname = QLabel('', objectName='DetailValue')
        billingLastnameColumn.addWidget(QLabel('Last name'))
        billingLastnameColumn.addWidget(self.billingLastname)
        # - company
        self.billingCompany = QLabel('', objectName='DetailValue')
        self.billing.addWidget(QLabel('Company'))
        self.billing.addWidget(self.billingCompany)
        # - email and phone
        billingEmailPhoneRow = QHBoxLayout()
        self.billing.addLayout(billingEmailPhoneRow)
        billingEmailColumn = QVBoxLayout()
        billingPhoneColumn = QVBoxLayout()
        billingEmailPhoneRow.addLayout(billingEmailColumn)
        billingEmailPhoneRow.addLayout(billingPhoneColumn)
        # -- email
        self.billingEmail = QLabel('', objectName='DetailValue')
        billingEmailColumn.addWidget(QLabel('Email'))
        billingEmailColumn.addWidget(self.billingEmail)
        # -- phone
        self.billingPhone = QLabel('', objectName='DetailValue')
        billingPhoneColumn.addWidget(QLabel('Phone'))
        billingPhoneColumn.addWidget(self.billingPhone)
        # - country and state
        billingCountryStateRow = QHBoxLayout()
        self.billing.addLayout(billingCountryStateRow)
        billingCountryColumn = QVBoxLayout()
        billingStateColumn = QVBoxLayout()
        billingCountryStateRow.addLayout(billingCountryColumn)
        billingCountryStateRow.addLayout(billingStateColumn)
        # -- country
        self.billingCountry = QLabel('', objectName='DetailValue')
        billingCountryColumn.addWidget(QLabel('Country'))
        billingCountryColumn.addWidget(self.billingCountry)
        # -- state
        self.billingState = QLabel('', objectName='DetailValue')
        billingStateColumn.addWidget(QLabel('State'))
        billingStateColumn.addWidget(self.billingState)
        # - city and postcode
        billingCityPostcodeRow = QHBoxLayout()
        self.billing.addLayout(billingCityPostcodeRow)
        billingCityColumn = QVBoxLayout()
        billingPostcodeColumn = QVBoxLayout()
        billingCityPostcodeRow.addLayout(billingCityColumn)
        billingCityPostcodeRow.addLayout(billingPostcodeColumn)
        # -- city
        self.billingCity = QLabel('Mashhad', objectName='DetailValue')
        billingCityColumn.addWidget(QLabel('City'))
        billingCityColumn.addWidget(self.billingCity)
        # -- postcode
        self.billingPostcode = QLabel('', objectName='DetailValue')
        billingPostcodeColumn.addWidget(QLabel('PostCode'))
        billingPostcodeColumn.addWidget(self.billingPostcode)
        # - address line 1
        self.billingAddressLine1 = QLabel('', objectName='DetailValue')
        self.billing.addWidget(QLabel('Address line 1'))
        self.billing.addWidget(self.billingAddressLine1)
        # - address line 2
        self.billingAddressLine2 = QLabel('', objectName='DetailValue')
        self.billing.addWidget(QLabel('Address line 2'))
        self.billing.addWidget(self.billingAddressLine2)
        # - payment and transaction
        billingPaymentTransactionRow = QHBoxLayout()
        self.billing.addLayout(billingPaymentTransactionRow)
        billingPaymentColumn = QVBoxLayout()
        billingTransactionColumn = QVBoxLayout()
        billingPaymentTransactionRow.addLayout(billingPaymentColumn)
        billingPaymentTransactionRow.addLayout(billingTransactionColumn)
        # -- payment
        self.billingPayment = QLabel('Cash on delivery', objectName='DetailValue')
        billingPaymentColumn.addWidget(QLabel('Payment method'))
        billingPaymentColumn.addWidget(self.billingPayment)
        # -- transaction
        self.billingTransaction = QLabel('', objectName='DetailValue')
        billingTransactionColumn.addWidget(QLabel('Transaction ID'))
        billingTransactionColumn.addWidget(self.billingTransaction)
        # add stretch
        self.billing.addStretch(1)

        # shipping
        self.shipping = QVBoxLayout()
        self.detailsLayout.addLayout(self.shipping)
        # - title
        self.shippingTitle = QLabel('Shipping', objectName='SectionTitle')
        self.shipping.addWidget(self.shippingTitle)
        # - first name and last name
        shippingFullnameRow = QHBoxLayout()
        self.shipping.addLayout(shippingFullnameRow)
        shippingFirstnameColumn = QVBoxLayout()
        shippingLastnameColumn = QVBoxLayout()
        shippingFullnameRow.addLayout(shippingFirstnameColumn)
        shippingFullnameRow.addLayout(shippingLastnameColumn)
        # -- first name
        self.shippingFirstname = QLabel('', objectName='DetailValue')
        shippingFirstnameColumn.addWidget(QLabel('First name'))
        shippingFirstnameColumn.addWidget(self.shippingFirstname)
        # -- last name
        self.shippingLastname = QLabel('', objectName='DetailValue')
        shippingLastnameColumn.addWidget(QLabel('Last name'))
        shippingLastnameColumn.addWidget(self.shippingLastname)
        # - company
        self.shippingCompany = QLabel('', objectName='DetailValue')
        self.shipping.addWidget(QLabel('Company'))
        self.shipping.addWidget(self.shippingCompany)
        # - country and state
        shippingCountryStateRow = QHBoxLayout()
        self.shipping.addLayout(shippingCountryStateRow)
        shippingCountryColumn = QVBoxLayout()
        shippingStateColumn = QVBoxLayout()
        shippingCountryStateRow.addLayout(shippingCountryColumn)
        shippingCountryStateRow.addLayout(shippingStateColumn)
        # -- country
        self.shippingCountry = QLabel('', objectName='DetailValue')
        shippingCountryColumn.addWidget(QLabel('Country'))
        shippingCountryColumn.addWidget(self.shippingCountry)
        # -- state
        self.shippingState = QLabel('', objectName='DetailValue')
        shippingStateColumn.addWidget(QLabel('State'))
        shippingStateColumn.addWidget(self.shippingState)
        # - city and postcode
        shippingCityPostcodeRow = QHBoxLayout()
        self.shipping.addLayout(shippingCityPostcodeRow)
        shippingCityColumn = QVBoxLayout()
        shippingPostcodeColumn = QVBoxLayout()
        shippingCityPostcodeRow.addLayout(shippingCityColumn)
        shippingCityPostcodeRow.addLayout(shippingPostcodeColumn)
        # -- city
        self.shippingCity = QLabel('', objectName='DetailValue')
        shippingCityColumn.addWidget(QLabel('City'))
        shippingCityColumn.addWidget(self.shippingCity)
        # -- postcode
        self.shippingPostcode = QLabel('', objectName='DetailValue')
        shippingPostcodeColumn.addWidget(QLabel('PostCode'))
        shippingPostcodeColumn.addWidget(self.shippingPostcode)
        # - address line 1
        self.shippingAddressLine1 = QLabel('', objectName='DetailValue')
        self.shipping.addWidget(QLabel('Address line 1'))
        self.shipping.addWidget(self.shippingAddressLine1)
        # - address line 2
        self.shippingAddressLine2 = QLabel('', objectName='DetailValue')
        self.shipping.addWidget(QLabel('Address line 2'))
        self.shipping.addWidget(self.shippingAddressLine2)
        # - customer note
        self.shippingCustomerNote = QLabel('', objectName='ShippingCustomerNote')
        self.shipping.addWidget(QLabel('Customer provided note'))
        self.shipping.addWidget(self.shippingCustomerNote)
        # add stretch
        self.shipping.addStretch(1)

        #########################
        # Section2: Order Items #
        #########################
        # widget
        self.section2 = QWidget(objectName='Section')
        self.orderLayout.addWidget(self.section2)
        # layout
        self.layout2 = QVBoxLayout()
        self.section2.setLayout(self.layout2)
        # title
        self.itemsTitle = QLabel('Items', objectName='SectionTitle')
        self.layout2.addWidget(self.itemsTitle)
        self.itemsTable = Table(['ID', 'Name', 'Cost', 'Quantity', 'Totals'])
        self.itemsTable.setMinimumHeight(200)
        self.layout2.addWidget(self.itemsTable)

    def setupControl(self):
        self.btnRefund = QPushButton('Refund')
        self.btnComplete = QPushButton('Complete')
        self.btnSave = QPushButton('Save')
        self.btnCancel = QPushButton('Cancel')
        self.controlLayout.addWidget(self.btnRefund)
        self.controlLayout.addWidget(self.btnComplete)
        self.controlLayout.addWidget(self.btnSave)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        self.btnCancel.clicked.connect(self.close)

    def setStyles(self):
        self.setStyleSheet("""
            QScrollArea{
                border: none;
            }
            QPushButton{
                min-height: 25px;
            }
            #Section{
                background-color: white;
            }
            #OrderTitle{
                font-size: 15px;
                min-height: 40px;
                font-weight: bold;
            }
            #SectionTitle{
                font-size: 12px;
                min-height: 30px;
                font-weight: bold;
            }
            #DetailValue{
                padding: 5px;
                margin-right: 5px;
                border-radius: 3px;
                border: 1px solid silver;
            }
            #ShippingCustomerNote{
                padding: 5px;
                min-height: 63px;
                min-width: 200px;
                margin-right: 5px;
                border-radius: 3px;
                border: 1px solid silver;
            }
        """)

    def setDetails(self, details):
        pass
