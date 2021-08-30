# internal
from src import connection
from src.translation import _
from src.models import Invoice
from src.ui.components import Message, Confirm


class Invoices(object):
    """Invoices View"""
    def __init__(self, ui):
        # cached orders
        self._orders = None
        # current
        self._current = dict()
        # invoice model
        self.invoice = Invoice()
        # ui
        self.ui = ui
        self.tab = ui.contents.invoices
        self.orders_table = self.tab.ordersTable
        self.invoices_table = self.tab.invoicesTable
        self.details = self.tab.orderDetails
        # connect signals
        self.ui.menu.btnInvoices.clicked.connect(self.tab_handler)
        self.tab.tabs.currentChanged.connect(self.tab_handler)
        # - orders tab
        self.tab.btnRefresh.clicked.connect(self.refresh)
        self.tab.btnSaveAll.clicked.connect(self.save_all)
        self.orders_table.itemDoubleClicked.connect(self.order_details)
        # - invoices tab
        self.tab.btnRemove.clicked.connect(self.remove)
        # - details
        self.details.btnUpdate.clicked.connect(self.update)
        self.details.btnSave.clicked.connect(self.save)

    def tab_handler(self):
        # find current tab const
        index = self.tab.tabs.currentIndex()
        if index == self.tab.ORDERS:
            self.get()
        else:
            self.get_saved()
        self.ui.contents.showTab(self.ui.contents.INVOICES)

    def get(self):
        if self._orders is None:
            conn = connection.get()
            self.invoice.set_connection(conn)
            try:
                raw_orders = self.invoice.orders()
            except Exception as e:
                msg = Message(self.ui, Message.ERROR, _('Cannot get orders from WooCommerce.'), str(e))
                msg.show()
            else:
                orders = dict()
                summary = list()
                for order in raw_orders:
                    orders[order['number']] = order
                    # generate summary
                    summary.append([
                        order['id'],
                        '#{} {} {}'.format(order['id'], order['first_name'], order['last_name']),
                        order['created_date'].strftime('%Y-%m-%d @ %H:%M:%S'),
                        order['status'],
                        order['total']
                    ])
                self._orders = orders
                self.orders_table.setRecords(reversed(summary))
            finally:
                conn.close()

    def refresh(self):
        # clear cache orders and call get method
        self._orders = None
        self.get()

    def order_details(self):
        index = self.orders_table.getCurrentRecordIndex()
        if index is not None:
            record = self.orders_table.getRecord(index)
            order = self._orders[record[0]]
            # save current order id and table's index
            self._current['number'] = order['number']
            self._current['index'] = index
            details = {
                'items': [
                    [item['id'],
                     item['name'],
                     item['price'],
                     item['quantity'],
                     item['total']]
                    for item in order['items']
                ],
                'totals': {
                    'order': order['total'],
                    'tax': order['total_tax'],
                    'items': order['items_subtotal'],
                    'shipping': order['shipping_total'],
                    'discount': order['discount_total']
                },
                'general': {
                    'status': order['status'],
                    'customer': order['customer_id'] or _('Guest'),
                    'date': order['created_date'].strftime('%Y-%m-%d @ %H:%M:%S')
                },
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
                }
            }
            self.details.setDetails(details)
            self.details.show()

    def update(self):
        status = self.details.getCurrentStatus()
        try:
            self.invoice.update_order(self._current['number'], {'status': status})
        except Exception as e:
            msg = Message(self.details, Message.ERROR, _('Cannot update order.'), str(e))
            msg.show()
        else:
            # update cached orders
            self._orders[self._current['number']]['status'] = status
            # update order details dialog
            self.details.changeStatus(status)
            # update order's summary table
            record = self.orders_table.getRecord(self._current['index'])
            record[3] = status
            self.orders_table.updateRecord(self._current['index'], record)
            msg = Message(self.details, Message.SUCCESS, _('Order updated successfully.'))
            msg.show()

    def save(self):
        conn = connection.get()
        self.invoice.set_connection(conn)
        order = self._orders[self._current['number']]
        try:
            self.invoice.save(order)
        except Exception as e:
            # rollback all changes
            conn.rollback()
            msg = Message(self.details, Message.ERROR, _('Cannot save order.'), str(e))
            msg.show()
        else:
            # commit all changes
            conn.commit()
            # update ui
            del self._orders[self._current['number']]
            self.orders_table.removeRecord(self._current['index'])
            # show success message
            msg = Message(self.details, Message.SUCCESS, _('Order saved successfully.'))
            msg.btnOk.clicked.connect(self.details.close)
            msg.show()
        finally:
            conn.close()

    def save_all(self):
        if self._orders is not None:
            completed = list()
            for order in self._orders.values():
                if order['status'] == 'completed':
                    completed.insert(0, order)
            if completed:
                # cache completed orders
                self._current['completed'] = completed
                # create confirm dialog
                plural = _('s ') if len(completed) > 1 else ' '
                details = _('{} order{}will be save.').format(len(completed), plural)
                confirm = Confirm(self.ui, Confirm.WARNING, _('Are you sure?'), details)
                confirm.btnOk.clicked.connect(self.save_all_confirm)
                confirm.show()
            else:
                msg = Message(self.ui, Message.ERROR, _('Order with completed status not found.'))
                msg.show()

    def save_all_confirm(self):
        error = False
        saves = 0
        conn = connection.get()
        self.invoice.set_connection(conn)
        for order in self._current['completed']:
            order_number = order['number']
            try:
                self.invoice.save(order)
            except Exception as e:
                conn.rollback()
                error = True
                message = _('Save progress interrupt by order #{}.').format(order_number)
                msg = Message(self.ui, Message.ERROR, message, str(e))
                msg.show()
                break
            else:
                conn.commit()
                saves += 1
                del self._orders[order_number]
                index = self.orders_table.findRecord(order_number)
                if index is not None:
                    self.orders_table.removeRecord(index)
        # close connection
        conn.close()
        # check for error
        if not error:
            plural = _('s ') if saves > 1 else ' '
            message = _('{} order{}saved successfully.').format(saves, plural)
            msg = Message(self.ui, Message.SUCCESS, message)
            msg.show()

    def get_saved(self):
        conn = connection.get()
        self.invoice.set_connection(conn)
        try:
            saved = self.invoice.saved()
        except Exception as e:
            msg = Message(self.ui, Message.ERROR, _('Cannot load saved invoices.'), str(e))
            msg.show()
        else:
            records = list()
            for invoice in saved:
                records.append([
                    invoice['No'],
                    '{} {}'.format(invoice['customer_code'], invoice['customer_name']),
                    invoice['order_id'],
                    invoice['saved_date'].strftime('%Y-%m-%d @ %H:%M:%S')
                ])
            self.invoices_table.setRecords(records)
        finally:
            conn.close()

    def remove(self):
        index = self.invoices_table.getCurrentRecordIndex()
        if index is not None:
            conn = connection.get()
            self.invoice.set_connection(conn)
            try:
                order_id = int(self.invoices_table.getRecord(index)[2])
                self.invoice.remove(order_id)
            except Exception as e:
                conn.rollback()
                msg = Message(self.ui, Message.ERROR, _('Cannot remove invoice.'), str(e))
                msg.show()
            else:
                conn.commit()
                self.invoices_table.removeRecord(index)
                msg = Message(self.ui, Message.SUCCESS, _('Invoice removed successfully.'))
                msg.show()
            finally:
                conn.close()
