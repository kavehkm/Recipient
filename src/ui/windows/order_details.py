# internal
from src.ui.components import BaseDialog
# pyqt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel


class OrderDetails(BaseDialog):
    """Order Details Dialog"""
    def setupDialog(self):
        # order title
        self.orderTitle = QLabel('Order #{} {} {}'.format(654, 'Kaveh', 'Mehrbanian'), objectName='OrderTitle')
        self.generalLayout.addWidget(self.orderTitle)

        # order details layouts
        self.orderDetailsLayout = QHBoxLayout()
        self.generalLayout.addLayout(self.orderDetailsLayout)

        # general details layout
        self.generalDetailsLayout = QVBoxLayout()
        self.orderDetailsLayout.addLayout(self.generalDetailsLayout, 1)
        # - title
        self.generalDetailsTitle = QLabel('General', objectName='OrderDetailsTitle')
        self.generalDetailsLayout.addWidget(self.generalDetailsTitle)
        # - date
        self.dateLabel = QLabel('Date created:', objectName='DetailLabel')
        self.dateValue = QLabel('{} @ {}:{}'.format('2021-07-03', 13, 56), objectName='DetailValue')
        self.generalDetailsLayout.addWidget(self.dateLabel)
        self.generalDetailsLayout.addWidget(self.dateValue)
        # - status
        self.statusLabel = QLabel('Status:', objectName='DetailLabel')
        self.statusValue = QLabel('Complete', objectName='DetailValue')
        self.generalDetailsLayout.addWidget(self.statusLabel)
        self.generalDetailsLayout.addWidget(self.statusValue)
        # - customer
        self.customerLabel = QLabel('Customer:', objectName='DetailLabel')
        self.customerValue = QLabel('Guest', objectName='DetailValue')
        self.generalDetailsLayout.addWidget(self.customerLabel)
        self.generalDetailsLayout.addWidget(self.customerValue)
        # add stretch
        self.generalDetailsLayout.addStretch(1)

        # billing details layout
        self.billingDetailsLayout = QVBoxLayout()
        self.orderDetailsLayout.addLayout(self.billingDetailsLayout, 2)
        # - title
        self.billingDetailsTitle = QLabel('Billing', objectName='OrderDetailsTitle')
        self.billingDetailsLayout.addWidget(self.billingDetailsTitle)
        # - first name and last name
        billingFullnametRow = QHBoxLayout()
        self.billingDetailsLayout.addLayout(billingFullnametRow)
        billingFirstnameColumn = QVBoxLayout()
        billingLastnameColumn = QVBoxLayout()
        billingFullnametRow.addLayout(billingFirstnameColumn)
        billingFullnametRow.addLayout(billingLastnameColumn)
        # -- first name
        self.billingFnameLabel = QLabel('First name', objectName='DetailLabel')
        self.billingFnameValue = QLabel('Kaveh', objectName='DetailValue')
        billingFirstnameColumn.addWidget(self.billingFnameLabel)
        billingFirstnameColumn.addWidget(self.billingFnameValue)
        # -- last name
        self.billingLnameLabel = QLabel('Last name', objectName='DetailLabel')
        self.billingLnameValue = QLabel('Mehrbanian', objectName='DetailValue')
        billingLastnameColumn.addWidget(self.billingLnameLabel)
        billingLastnameColumn.addWidget(self.billingLnameValue)
        # - company
        self.billingCompanyLabel = QLabel('Company', objectName='DetailLabel')
        self.billingCompanyValue = QLabel('', objectName='DetailValue')
        self.billingDetailsLayout.addWidget(self.billingCompanyLabel)
        self.billingDetailsLayout.addWidget(self.billingCompanyValue)
        # - email and phone
        billingEmailPhoneRow = QHBoxLayout()
        self.billingDetailsLayout.addLayout(billingEmailPhoneRow)
        billingEmailColumn = QVBoxLayout()
        billingPhoneColumn = QVBoxLayout()
        billingEmailPhoneRow.addLayout(billingEmailColumn)
        billingEmailPhoneRow.addLayout(billingPhoneColumn)
        # -- email
        self.billingEmailLabel = QLabel('Email', objectName='DetailLabel')
        self.billingEmailValue = QLabel('Mehrbaniankaveh@gmail.com', objectName='DetailValue')
        billingEmailColumn.addWidget(self.billingEmailLabel)
        billingEmailColumn.addWidget(self.billingEmailValue)
        # -- phone
        self.billingPhoneLabel = QLabel('Phone', objectName='DetailLabel')
        self.billingPhoneValue = QLabel('09372542368', objectName='DetailValue')
        billingPhoneColumn.addWidget(self.billingPhoneLabel)
        billingPhoneColumn.addWidget(self.billingPhoneValue)
        # - country and state
        billingCountryStateRow = QHBoxLayout()
        self.billingDetailsLayout.addLayout(billingCountryStateRow)
        billingCountryColumn = QVBoxLayout()
        billingStateColumn = QVBoxLayout()
        billingCountryStateRow.addLayout(billingCountryColumn)
        billingCountryStateRow.addLayout(billingStateColumn)
        # -- country
        self.billingCountryLabel = QLabel('Country / Region', objectName='DetailLabel')
        self.billingCountryValue = QLabel('Iran', objectName='DetailValue')
        billingCountryColumn.addWidget(self.billingCountryLabel)
        billingCountryColumn.addWidget(self.billingCountryValue)
        # -- state
        self.billingStateLabel = QLabel('State / County', objectName='DetailLabel')
        self.billingStateValue = QLabel('Razavi Khorasan', objectName='DetailValue')
        billingStateColumn.addWidget(self.billingStateLabel)
        billingStateColumn.addWidget(self.billingStateValue)
        # - city and postcode
        billingCityPostcodeRow = QHBoxLayout()
        self.billingDetailsLayout.addLayout(billingCityPostcodeRow)
        billingCityColumn = QVBoxLayout()
        billingPostcodeColumn = QVBoxLayout()
        billingCityPostcodeRow.addLayout(billingCityColumn)
        billingCityPostcodeRow.addLayout(billingPostcodeColumn)
        # -- city
        self.billingCityLabel = QLabel('City', objectName='DetailLabel')
        self.billingCityValue = QLabel('Mashhad', objectName='DetailValue')
        billingCityColumn.addWidget(self.billingCityLabel)
        billingCityColumn.addWidget(self.billingCityValue)
        # -- postcode
        self.billingPostcodeLabel = QLabel('PostCode / Zip', objectName='DetailLabel')
        self.billingPostcodeValue = QLabel('', objectName='DetailValue')
        billingPostcodeColumn.addWidget(self.billingPostcodeLabel)
        billingPostcodeColumn.addWidget(self.billingPostcodeValue)
        # - address line 1
        self.billingAddressLine1Label = QLabel('Address line 1', objectName='DetailLabel')
        self.billingAddressLine1Value = QLabel('', objectName='DetailValue')
        self.billingDetailsLayout.addWidget(self.billingAddressLine1Label)
        self.billingDetailsLayout.addWidget(self.billingAddressLine1Value)
        # - address line 2
        self.billingAddressLine2Label = QLabel('Address line 2', objectName='DetailLabel')
        self.billingAddressLine2Value = QLabel('', objectName='DetailValue')
        self.billingDetailsLayout.addWidget(self.billingAddressLine2Label)
        self.billingDetailsLayout.addWidget(self.billingAddressLine2Value)
        # - payment and transaction
        billingPaymentTransactionRow = QHBoxLayout()
        self.billingDetailsLayout.addLayout(billingPaymentTransactionRow)
        billingPaymentColumn = QVBoxLayout()
        billingTransactionColumn = QVBoxLayout()
        billingPaymentTransactionRow.addLayout(billingPaymentColumn)
        billingPaymentTransactionRow.addLayout(billingTransactionColumn)
        # -- payment
        self.billingPaymentLabel = QLabel('Payment method', objectName='DetailLabel')
        self.billingPaymentValue = QLabel('Cash on delivery', objectName='DetailValue')
        billingPaymentColumn.addWidget(self.billingPaymentLabel)
        billingPaymentColumn.addWidget(self.billingPaymentValue)
        # -- transaction
        self.billingTransactionLabel = QLabel('Transaction ID', objectName='DetailLabel')
        self.billingTransactionValue = QLabel('', objectName='DetailValue')
        billingTransactionColumn.addWidget(self.billingTransactionLabel)
        billingTransactionColumn.addWidget(self.billingTransactionValue)
        # add stretch
        self.billingDetailsLayout.addStretch(1)

        # shipping details layout
        self.shippingDetailsLayout = QVBoxLayout()
        self.orderDetailsLayout.addLayout(self.shippingDetailsLayout, 2)
        # - title
        self.shippingDetailsTitle = QLabel('Shipping', objectName='OrderDetailsTitle')
        self.shippingDetailsLayout.addWidget(self.shippingDetailsTitle)
        # add stretch
        self.shippingDetailsLayout.addStretch(1)

    def setupControl(self):
        pass

    def connectSignals(self):
        pass

    def setStyles(self):
        self.setStyleSheet("""
            #OrderTitle{
                font-size: 20px;
                min-height: 70px;
            }
            #OrderDetailsTitle{
                font-size: 12px;
                font-weight: bold;
                min-height: 40px;
            }
            #DetailLabel{
            
            }
            #DetailValue{
                padding: 5px;
                margin-right: 5px;
                border: 1px solid silver;
                border-radius: 3px;
            }
        """)

    def setDetails(self, details):
        pass
        self.update()
