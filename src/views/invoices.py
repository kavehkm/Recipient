# standard
from datetime import datetime
# internal
from src import wc, db, models
from src.ui.components import Message
from src.models.errors import DoesNotExistsError


class Invoices(object):
    """Invoices View"""
    def __init__(self, ui):
        # cached orders
        self._orders = None
        # cached orders summary
        self._summary = None
        # current order on details
        self._current = dict()

        # wc order model
        self.wc_order = wc.Order()
        # moein models
        self.product = models.Product()
        self.product_map = models.ProductMap()
        self.customer = models.Customer()
        self.customer_map = models.CustomerMap()
        self.invoice = models.Invoice()
        self.item_line = models.ItemLine()
        self.saved_order = models.SavedOrder()

        # ui
        self.ui = ui
        self.tab = ui.contents.invoices
        self.table = self.tab.invoicesTable
        self.details = self.tab.orderDetails

        # connect signals
        self.ui.menu.btnInvoices.clicked.connect(self.tab_handler)
        # - tab
        self.tab.btnRefresh.clicked.connect(self.refresh)
        self.tab.btnSaveAll.clicked.connect(self.save_all)
        self.table.itemDoubleClicked.connect(self.order_details)
        # - details
        self.details.btnUpdate.clicked.connect(self.update)
        self.details.btnSave.clicked.connect(self.save)

    def tab_handler(self):
        self.get()
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    @staticmethod
    def _firstname(order):
        return order['billing']['first_name'] or order['shipping']['first_name']

    @staticmethod
    def _lastname(order):
        return order['billing']['last_name'] or order['shipping']['last_name']

    @staticmethod
    def _created_date(order):
        gmt = datetime.fromisoformat(order['date_created_gmt'])
        return '{} @ {}'.format(gmt.date().isoformat(), gmt.time().isoformat())

    @staticmethod
    def _items_total(order):
        items_total = 0
        for item in order['line_items']:
            items_total += int(item['subtotal'])
        return items_total

    def _items(self, conn, order):
        items = []
        self.product.connection = conn
        self.product_map.connection = conn
        for item in order['line_items']:
            product_id = item['product_id']
            moein_id = self.product_map.get('id', wcid=product_id).id
            moein_product = self.product.get('name', id=moein_id)
            items.append({
                'id': moein_id,
                'name': moein_product.name,
                'price': item['price'],
                'quantity': item['quantity'],
                # before discounts
                'subtotal': item['subtotal'],
                # after discounts
                'total': item['total']
            })
        return items

    def _order_key(self, order):
        return '#{} {} {}'.format(order['id'], self._firstname(order), self._lastname(order))

    def get(self):
        if self._orders is None:
            try:
                # find saved order to exclude
                with db.connection() as conn:
                    self.saved_order.connection = conn
                    ids = [order.id for order in self.saved_order.all('id')]
                raw_orders = self.wc_order.all(excludes=ids)
            except Exception as e:
                msg = Message(self.ui, Message.ERROR, 'Cannot get orders from WooCommerce.', str(e))
                msg.show()
                return
            else:
                self._orders, self._summary = {}, []
                # set up cached orders and summary
                for order in raw_orders:
                    self._orders[order['number']] = order
                    self._summary.insert(0, [
                        order['id'],
                        self._order_key(order),
                        self._created_date(order),
                        order['status'],
                        order['total']
                    ])
        self.table.setRecords(self._summary)

    def refresh(self):
        # clear cache orders and call get method
        self._orders = None
        self.get()

    def order_details(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            try:
                record = self.table.getRecord(index)
                order = self._orders[record[0]]
                # get mapped product as items
                with db.connection() as conn:
                    items = self._items(conn, order)
                # save current order and all relative information for later...
                self._current['order'] = order
                self._current['items'] = items
                self._current['index'] = index
                # collect details from order
                details = {
                    # general
                    'general': {
                        'date': self._created_date(order),
                        'status': order['status'],
                        'customer': order['customer_id'] or 'Guest',
                    },
                    # billing
                    'billing': {
                        'firstname': order['billing']['first_name'],
                        'lastname': order['billing']['last_name'],
                        'company': order['billing']['company'],
                        'email': order['billing']['email'],
                        'phone': order['billing']['phone'],
                        'country': order['billing']['country'],
                        'state': order['billing']['state'],
                        'city': order['billing']['city'],
                        'postcode': order['billing']['postcode'],
                        'address1': order['billing']['address_1'],
                        'address2': order['billing']['address_2'],
                        'payment': order['payment_method_title'],
                        'transaction': order['transaction_id']
                    },
                    # shipping
                    'shipping': {
                        'firstname': order['shipping']['first_name'],
                        'lastname': order['shipping']['last_name'],
                        'company': order['shipping']['company'],
                        'country': order['shipping']['country'],
                        'state': order['shipping']['state'],
                        'city': order['shipping']['city'],
                        'postcode': order['shipping']['postcode'],
                        'address1': order['shipping']['address_1'],
                        'address2': order['shipping']['address_2'],
                        'note': order['customer_note']
                    },
                    # totals
                    'totals': {
                        'tax': order['total_tax'],
                        'shipping': order['shipping_total'],
                        'discount': order['discount_total'],
                        'order': order['total'],
                        'items': self._items_total(order)
                    },
                    # items
                    'items': [
                        [i['id'], i['name'], i['price'], i['quantity'], i['total']]
                        for i in items
                    ]
                }
            except Exception as e:
                msg = Message(self.ui, Message.ERROR, 'Cannot load order details.', str(e))
                msg.show()
            else:
                self.details.setDetails(details)
                self.details.show()

    def update(self):
        status = self.details.getCurrentStatus()
        order_id = self._current['order']['number']
        try:
            self.wc_order.update(order_id, {'status': status})
        except Exception as e:
            msg = Message(self.details, Message.ERROR, 'Cannot update order.', str(e))
            msg.show()
        else:
            # update cached orders
            self._orders[order_id]['status'] = status
            # update summary
            self._summary[self._current['index']][3] = status
            # update order on details-dialog
            self.details.changeStatus(status)
            # update invoices table
            record = self.table.getRecord(self._current['index'])
            record[3] = status
            self.table.updateRecord(self._current['index'], record)
            msg = Message(self.details, Message.SUCCESS, 'Order updated successfully.')
            msg.show()

    def _saver(self, conn, order, items, index):
        # set models connection
        self.customer.connection = conn
        self.customer_map.connection = conn
        self.invoice.connection = conn
        self.item_line.connection = conn
        self.saved_order.connection = conn
        # detect customer
        wc_customer_id = order['customer_id']
        if wc_customer_id == 0:
            # customer is guest
            moein_customer_id = 44
        else:
            try:
                moein_customer = self.customer_map.get('id', wcid=wc_customer_id)
            except DoesNotExistsError:
                # customer does not exists, lets create
                self.customer.create({
                    'firstname': self._firstname(order),
                    'lastname': self._lastname(order)
                })
                # get created_customer's id
                moein_customer_id = self.customer.get_max_pk()
                # map moein-customer with woocommerce-customer
                self.customer_map.create({
                    'id': moein_customer_id,
                    'wcid': wc_customer_id,
                    'last_update': datetime.now()
                })
            else:
                moein_customer_id = moein_customer.id
        # create invoice
        self.invoice.create({
            'customer_id': moein_customer_id,
            'created_date': datetime.fromisoformat(order['date_created'])
        })
        # get created_invoice's id
        invoice_id = self.invoice.get_max_pk()
        # set invoice items
        for item in items:
            self.item_line.create({
                'invoice_id': invoice_id,
                'product_id': item['id'],
                'quantity': item['quantity']
            })
        # save order
        self.saved_order.create({
            'id': order['id'],
            'invoice_id': invoice_id
        })
        # update ui after save
        # - remove from cached orders
        del self._orders[order['number']]
        # - remove from cached orders summary
        del self._summary[index]
        # - remove from invoices table
        self.table.removeRecord(index)

    def save(self):
        try:
            with db.connection() as conn:
                self._saver(conn, self._current['order'], self._current['items'], self._current['index'])
                conn.commit()
        except Exception as e:
            msg = Message(self.details, Message.ERROR, 'Cannot save order.', str(e))
            msg.show()
        else:
            msg = Message(self.details, Message.SUCCESS, 'Order saved successfully.')
            msg.btnOk.clicked.connect(self.details.close)
            msg.show()

    def save_all(self):
        pass
