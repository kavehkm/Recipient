# internal
from src.ui.components import BaseDialog, Table, ScrollArea, MDCombo, CancelMDButton, SaveMDButton, SyncMDButton
# pyqt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLabel


class OrderDetails(BaseDialog):
    """Order Details Dialog"""
    # order status
    PENDING =       'pending'
    FAILED =        'failed'
    PROCESSING =    'processing'
    COMPLETED =     'completed'
    ON_HOLD =       'on-hold'
    CANCELLED =     'cancelled'
    REFUNDED =      'refunded'
    # statuses
    STATUSES = [
        PENDING,
        FAILED,
        PROCESSING,
        COMPLETED,
        ON_HOLD,
        CANCELLED,
        REFUNDED
    ]

    def setupLayout(self):
        super().setupLayout()
        # set dialog title
        self.setWindowTitle('Order details')
        # set dialog minimum size
        self.setMinimumSize(900, 562)

    def setupDialog(self):
        # scrollable area
        self.scrollableArea = ScrollArea()
        self.dialogLayout.addWidget(self.scrollableArea)
        # order layout
        self.orderLayout = QVBoxLayout()
        self.orderLayout.setSpacing(20)
        self.scrollableArea.setLayout(self.orderLayout)

        ###########################
        # Section1: Order Details #
        ###########################
        # widget
        self.section1 = QWidget(objectName='Section')
        self.orderLayout.addWidget(self.section1)
        # layout
        self.layout1 = QVBoxLayout()
        self.section1.setLayout(self.layout1)
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
        self.dateCreated = QLabel(objectName='DetailValue')
        self.general.addWidget(QLabel('Date created:'))
        self.general.addWidget(self.dateCreated)
        # - customer
        self.customer = QLabel(objectName='DetailValue')
        self.general.addWidget(QLabel('Customer:'))
        self.general.addWidget(self.customer)
        # - status
        self.status = QLabel(objectName='OrderStatus')
        self.general.addWidget(QLabel('Status:'))
        self.general.addWidget(self.status)
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
        self.billingFirstname = QLabel(objectName='DetailValue')
        billingFirstnameColumn.addWidget(QLabel('First name'))
        billingFirstnameColumn.addWidget(self.billingFirstname)
        # -- last name
        self.billingLastname = QLabel(objectName='DetailValue')
        billingLastnameColumn.addWidget(QLabel('Last name'))
        billingLastnameColumn.addWidget(self.billingLastname)
        # - company
        self.billingCompany = QLabel(objectName='DetailValue')
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
        self.billingEmail = QLabel(objectName='DetailValue')
        billingEmailColumn.addWidget(QLabel('Email'))
        billingEmailColumn.addWidget(self.billingEmail)
        # -- phone
        self.billingPhone = QLabel(objectName='DetailValue')
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
        self.billingCountry = QLabel(objectName='DetailValue')
        billingCountryColumn.addWidget(QLabel('Country'))
        billingCountryColumn.addWidget(self.billingCountry)
        # -- state
        self.billingState = QLabel(objectName='DetailValue')
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
        self.billingCity = QLabel(objectName='DetailValue')
        billingCityColumn.addWidget(QLabel('City'))
        billingCityColumn.addWidget(self.billingCity)
        # -- postcode
        self.billingPostcode = QLabel(objectName='DetailValue')
        billingPostcodeColumn.addWidget(QLabel('PostCode'))
        billingPostcodeColumn.addWidget(self.billingPostcode)
        # - address line 1
        self.billingAddressLine1 = QLabel(objectName='DetailValue')
        self.billing.addWidget(QLabel('Address line 1'))
        self.billing.addWidget(self.billingAddressLine1)
        # - address line 2
        self.billingAddressLine2 = QLabel(objectName='DetailValue')
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
        self.billingTransaction = QLabel(objectName='DetailValue')
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
        self.shippingFirstname = QLabel(objectName='DetailValue')
        shippingFirstnameColumn.addWidget(QLabel('First name'))
        shippingFirstnameColumn.addWidget(self.shippingFirstname)
        # -- last name
        self.shippingLastname = QLabel(objectName='DetailValue')
        shippingLastnameColumn.addWidget(QLabel('Last name'))
        shippingLastnameColumn.addWidget(self.shippingLastname)
        # - company
        self.shippingCompany = QLabel(objectName='DetailValue')
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
        self.shippingCountry = QLabel(objectName='DetailValue')
        shippingCountryColumn.addWidget(QLabel('Country'))
        shippingCountryColumn.addWidget(self.shippingCountry)
        # -- state
        self.shippingState = QLabel(objectName='DetailValue')
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
        self.shippingCity = QLabel(objectName='DetailValue')
        shippingCityColumn.addWidget(QLabel('City'))
        shippingCityColumn.addWidget(self.shippingCity)
        # -- postcode
        self.shippingPostcode = QLabel(objectName='DetailValue')
        shippingPostcodeColumn.addWidget(QLabel('PostCode'))
        shippingPostcodeColumn.addWidget(self.shippingPostcode)
        # - address line 1
        self.shippingAddressLine1 = QLabel(objectName='DetailValue')
        self.shipping.addWidget(QLabel('Address line 1'))
        self.shipping.addWidget(self.shippingAddressLine1)
        # - address line 2
        self.shippingAddressLine2 = QLabel(objectName='DetailValue')
        self.shipping.addWidget(QLabel('Address line 2'))
        self.shipping.addWidget(self.shippingAddressLine2)
        # - customer note
        self.shippingCustomerNote = QLabel(objectName='ShippingCustomerNote')
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
        # table
        self.itemsTable = Table(['ID', 'Name', 'Cost', 'Quantity', 'Total'], [1, 3, 1, 1, 1])
        self.itemsTable.setMinimumHeight(200)
        self.layout2.addWidget(self.itemsTable)

        ##########################
        # Section3: Order Totals #
        ##########################
        # widget
        self.section3 = QWidget(objectName='Section')
        self.orderLayout.addWidget(self.section3)
        # layout
        self.layout3 = QVBoxLayout()
        self.section3.setLayout(self.layout3)
        # title
        self.totalsTitle = QLabel('Totals', objectName='SectionTitle')
        self.layout3.addWidget(self.totalsTitle)
        # form
        self.totalsForm = QFormLayout()
        self.totalsForm.setHorizontalSpacing(50)
        self.totalsForm.setVerticalSpacing(20)
        self.layout3.addLayout(self.totalsForm)
        # order items total
        self.itemsTotal = QLabel()
        self.totalsForm.addRow(QLabel('Items total'), self.itemsTotal)
        # order total tax
        self.totalTax = QLabel()
        self.totalsForm.addRow(QLabel('Total tax'), self.totalTax)
        # order shipping total
        self.shippingTotal = QLabel()
        self.totalsForm.addRow(QLabel('Shipping total'), self.shippingTotal)
        # order discount total
        self.discountTotal = QLabel()
        self.totalsForm.addRow(QLabel('Discount total'), self.discountTotal)
        # order total
        self.orderTotal = QLabel()
        self.totalsForm.addRow(QLabel('<b>Order total</b>'), self.orderTotal)

    def setupControl(self):
        # status combo box
        self.comboStatus = MDCombo()
        self.comboStatus.addItems(self.STATUSES)
        # update button
        self.btnUpdate = SyncMDButton('Update')
        # save button
        self.btnSave = SaveMDButton('Save')
        # - hide save button as default
        self.btnSave.hide()
        # cancel button
        self.btnCancel = CancelMDButton('Cancel')
        # register combo and buttons
        self.controlLayout.addWidget(self.comboStatus)
        self.controlLayout.addWidget(self.btnUpdate)
        self.controlLayout.addWidget(self.btnSave)
        self.controlLayout.addWidget(self.btnCancel)

    def connectSignals(self):
        self.btnCancel.clicked.connect(self.close)

    def setStyles(self):
        self.setStyleSheet("""
            #Section{
                background-color: white;
            }
            #SectionTitle{
                font-size: 13px;
                min-height: 40px;
                font-weight: bold;
            }
            #DetailValue{
                padding: 5px;
                margin-right: 5px;
                border-radius: 3px;
                border: 1px solid silver;
            }
            #OrderStatus{
                padding: 5px;
                margin-right: 5px;
                border-radius: 3px;
                border: 1px solid silver;
                font-size: 12px;
                font-weight: bold;
                min-height: 30px;
            }
            #OrderStatus[status="pending"]{
                background-color: #E5E5E5;
            }
            #OrderStatus[status="failed"]{
                background-color: #ECA3A3;
            }
            #OrderStatus[status="processing"]{
                background-color: #C6E2C6;
            }
            #OrderStatus[status="completed"]{
                background-color: #C9D7E1;
            }
            #OrderStatus[status="on-hold"]{
                background-color: #F8DEA7;
            }
            #OrderStatus[status="cancelled"]{
                background-color: #E5E5E5;
            }
            #OrderStatus[status="refunded"]{
                background-color: #E5E5E5;
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

    def getCurrentStatus(self):
        return self.comboStatus.currentText()

    def changeStatus(self, status):
        if status in self.STATUSES:
            # change value and style of status field
            self.status.setText(status)
            self.status.setProperty('status', status)
            self.status.setStyleSheet(self.status.styleSheet())
            # set current status for comboStatus
            self.comboStatus.setCurrentText(status)
            # if status is completed show save button
            if status == self.COMPLETED:
                self.btnSave.show()
            else:
                self.btnSave.hide()

    def setDetails(self, details):
        # general
        general = details.get('general', {})
        general_fields = {
            'date': self.dateCreated,
            'status': self.status,
            'customer': self.customer,
        }
        for name, field in general_fields.items():
            value = general.get(name, '')
            getattr(field, 'setText')(str(value))
        # billing
        billing = details.get('billing', {})
        billing_fields = {
            'firstname': self.billingFirstname,
            'lastname': self.billingLastname,
            'company': self.billingCompany,
            'email': self.billingEmail,
            'phone': self.billingPhone,
            'country': self.billingCountry,
            'state': self.billingState,
            'city': self.billingCity,
            'postcode': self.billingPostcode,
            'address1': self.billingAddressLine1,
            'address2': self.billingAddressLine2,
            'payment': self.billingPayment,
            'transaction': self.billingTransaction
        }
        for name, field in billing_fields.items():
            value = billing.get(name, '')
            getattr(field, 'setText')(str(value))
        # shipping
        shipping = details.get('shipping', {})
        shipping_fields = {
            'firstname': self.shippingFirstname,
            'lastname': self.shippingLastname,
            'company': self.shippingCompany,
            'country': self.shippingCountry,
            'state': self.shippingState,
            'city': self.shippingCity,
            'postcode': self.shippingPostcode,
            'address1': self.shippingAddressLine1,
            'address2': self.shippingAddressLine2,
            'note': self.shippingCustomerNote
        }
        for name, field in shipping_fields.items():
            value = shipping.get(name, '')
            getattr(field, 'setText')(str(value))
        # items
        items = details.get('items', [])
        self.itemsTable.setRecords(items)
        # totals
        totals = details.get('totals', {})
        totals_fields = {
            'items': self.itemsTotal,
            'tax': self.totalTax,
            'shipping': self.shippingTotal,
            'discount': self.discountTotal,
            'order': self.orderTotal
        }
        for name, field in totals_fields.items():
            value = totals.get(name, '')
            getattr(field, 'setText')(str(value))

        # set order status
        self.changeStatus(general['status'])
