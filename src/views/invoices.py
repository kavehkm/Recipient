# standard
from datetime import datetime
# internal
from src import wc, db, models
from src.ui.components import Message


class Invoices(object):
    """Invoices View"""
    def __init__(self, ui):
        # orders
        self._orders = None
        # current order on details
        self._current_order = None
        self._current_record_index = None
        self._current_summary_index = None

        # wc order model
        self.wc_order = wc.Order()
        # moein product and map models
        self.product = models.Product()
        self.product_map = models.ProductMap()

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

    def _order_key(self, order):
        return '#{} {} {}'.format(order['id'], self._firstname(order), self._lastname(order))

    def get(self):
        if self._orders is None:
            try:
                raw_orders = self.wc_order.all()
            except Exception as e:
                msg = Message(self.ui, Message.ERROR, 'Cannot get orders from WooCommerce.', str(e))
                msg.show()
                return
            else:
                self._orders = {
                    order['number']: order
                    for order in raw_orders
                }
                # create orders summary for invoices table
                self._orders['summary'] = [
                    [order['id'],
                     self._order_key(order),
                     self._created_date(order),
                     order['status'],
                     order['total']]
                    for order in raw_orders
                ]
        self.table.setRecords(self._orders['summary'])

    def refresh(self):
        self._orders = None
        self.get()

    def save_all(self):
        pass

    def order_details(self):
        index = self.table.getCurrentRecordIndex()
        if index is not None:
            try:
                record = self.table.getRecord(index)
                order = self._orders.get(record[0])
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
                        'order': order['total']
                    }
                }
                # compute items-total
                items_total = 0
                for item in order['line_items']:
                    items_total += int(item['subtotal'])
                details['totals']['items'] = items_total

                # prepare items
                items = []
                with db.connection() as conn:
                    self.product.connection = self.product_map.connection = conn
                    for item in order['line_items']:
                        product_id = item['product_id']
                        moein_id = self.product_map.get('id', wcid=product_id).id
                        moein_product = self.product.get('name', id=moein_id)
                        items.append([
                            moein_id,
                            moein_product.name,
                            item['price'],
                            item['quantity'],
                            item['subtotal']
                        ])
                details['items'] = items
                # save current order and record for later ...
                self._current_order = order
                self._current_record_index = index
                # compute current record index in self._orders['summary']
                self._current_summary_index = len(self._orders['summary']) - index - 1
            except Exception as e:
                msg = Message(self.ui, Message.ERROR, 'Cannot load order details.', str(e))
                msg.show()
            else:
                self.details.setDetails(details)
                self.details.show()

    def update(self):
        status = self.details.getCurrentStatus()
        order_id = self._current_order['number']
        try:
            data = {
                'status': status
            }
            self.wc_order.update(order_id, data)
        except Exception as e:
            msg = Message(self.details, Message.ERROR, 'Cannot update order.', str(e))
            msg.show()
        else:
            # update cached orders
            self._orders[order_id]['status'] = status
            # update cached orders['summary']
            self._orders['summary'][self._current_summary_index][3] = status
            # update order on details-dialog
            self.details.changeStatus(status)
            # update invoices table
            record = self.table.getRecord(self._current_record_index)
            record[3] = status
            self.table.updateRecord(self._current_record_index, record)

            msg = Message(self.details, Message.SUCCESS, 'Order updated successfully.')
            msg.show()

    def save(self):
        pass
