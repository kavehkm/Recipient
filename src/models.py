# standard
from datetime import datetime
# internal
from src import table
from src import wc_api
from src import wc
from src import settings as s


class Model(object):
    """Recipient Model"""
    def __init__(self):
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection


class Mappable(Model):
    """Recipient Mappable"""
    def mapped(self):
        pass

    def unmapped(self):
        pass

    def wc_mapped(self):
        pass

    def wc_unmapped(self):
        pass

    def wc_mapped_update(self, mapped):
        pass

    def add_map(self, moeinid, wcid, last_update):
        pass

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        pass

    def remove_map(self, moeinid):
        pass

    def export2wc(self, moein_object):
        pass

    def import2moein(self, wc_object):
        pass


class Product(Mappable):
    """Recipeint Product Model"""
    def __init__(self):
        super().__init__()
        # product table
        self.p = table.get('Product', 'id')
        # product map table
        self.pm = table.get('ProductMap', 'id')
        # category map table
        self.cm = table.get('CategoryMap', 'id')
        # wc product
        api = wc_api.get()
        self.wcp = wc.get(api, 'products')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.p.set_connection(connection)
        self.pm.set_connection(connection)
        self.cm.set_connection(connection)

    def mapped(self):
        mapped = []
        rows = self.p.inner_join(
            self.pm,
            'id',
            'id',
            [],
            ['wcid', 'last_update', 'update_required']
        )
        for row in rows:
            mapped.append({
                'id': row.id,
                'name': row.name,
                'price': row.price,
                'category_id': row.category_id,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = []
        rows = self.p.left_outer_join(
            self.pm,
            'id',
            'id',
            []
        )
        for row in rows:
            unmapped.append({
                'id': row.id,
                'name': row.name,
                'price': row.price,
                'category_id': row.category_id,
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.pm.all('wcid')
        ]

    def wc_unmapped(self):
        ids = [row.wcid for row in self.pm.all('wcid')]
        return self.wcp.all(excludes=ids)

    def wc_mapped_update(self, mapped):
        self.wcp.update(mapped['wcid'], {
            'name': mapped['name'],
            'regular_price': str(mapped['price'])
        })
        self.pm.update({'last_update': datetime.now()}, id=mapped['id'])

    def add_map(self, moeinid, wcid, last_update):
        # check moeinid
        product = self.p.get('id', 'name', id=moeinid)
        # check wcid
        self.wcp.get(wcid)
        # every thing is ok lets create map
        fields = {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        }
        self.pm.create(fields)
        # extends fields
        fields['name'] = product.name
        return fields

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check moeinid
        product = self.p.get('id', 'name', id=new_moeinid)
        # check wcid
        self.wcp.get(new_wcid)
        fields = {
            'id': new_moeinid,
            'wcid': new_wcid
        }
        self.pm.update(fields, id=moeinid)
        # extends fields
        fields['name'] = product.name
        return fields

    def remove_map(self, moeinid):
        # check moeinid
        self.pm.get(id=moeinid)
        # remove map
        self.pm.delete(id=moeinid)

    def export2wc(self, product):
        # find wc_category
        wc_category = self.cm.get('wcid', id=product['category_id'])
        wc_product = self.wcp.create({
            'name': product['name'],
            'regular_price': str(product['price']),
            'categories': [{'id': wc_category.wcid}]
        })
        self.pm.create({
            'id': product['id'],
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_product):
        # get first category
        wc_category = wc_product['categories'][0]
        category = self.cm.get('id', wcid=wc_category['id'])
        self.p.create({
            'name': wc_product['name'],
            'price': wc_product['regular_price'],
            'category_id': category.id
        })
        self.pm.create({
            'id': self.p.max_pk(),
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })


class Category(Mappable):
    """Recipient Category Model"""
    def __init__(self):
        super().__init__()
        # category table
        self.c = table.get('Category', 'id')
        # category map table
        self.cm = table.get('CategoryMap', 'id')
        # wc category
        api = wc_api.get()
        self.wcc = wc.get(api, 'products/categories')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.c.set_connection(connection)
        self.cm.set_connection(connection)

    def mapped(self):
        mapped = []
        rows = self.c.inner_join(
            self.cm,
            'id',
            'id',
            [],
            ['wcid', 'last_update', 'update_required']
        )
        for row in rows:
            mapped.append({
                'id': row.id,
                'name': row.name,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = []
        rows = self.c.left_outer_join(
            self.cm,
            'id',
            'id',
            []
        )
        for row in rows:
            unmapped.append({
                'id': row.id,
                'name': row.name
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.cm.all('wcid')
        ]

    def wc_unmapped(self):
        ids = [row.wcid for row in self.cm.all('wcid')]
        return self.wcc.all(excludes=ids)

    def wc_mapped_update(self, mapped):
        self.wcc.update(mapped['wcid'], {
            'name': mapped['name']
        })
        self.cm.update({'last_update': datetime.now()}, id=mapped['id'])

    def add_map(self, moeinid, wcid, last_update):
        # check moeinid
        category = self.c.get('id', 'name', id=moeinid)
        # check wcid
        self.wcc.get(wcid)
        fields = {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        }
        self.cm.create(fields)
        fields['name'] = category.name
        return fields

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check moeinid
        category = self.c.get('id', 'name', id=new_moeinid)
        # check wcid
        self.wcc.get(new_wcid)
        fields = {
            'id': new_moeinid,
            'wcid': new_wcid
        }
        self.cm.update(fields, id=moeinid)
        fields['name'] = category.name
        return fields

    def remove_map(self, moeinid):
        self.cm.get(id=moeinid)
        self.cm.delete(id=moeinid)

    def export2wc(self, category):
        wc_category = self.wcc.create({
            'parent': 0,
            'name': category['name']
        })
        self.cm.create({
            'id': category['id'],
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_category):
        self.c.create({
            'name': wc_category['name']
        })
        self.cm.create({
            'id': self.c.max_pk(),
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })


class Invoice(Model):
    """Recipient Invoice Model"""
    def __init__(self):
        super().__init__()
        # invoice table
        self.i = table.get('Invoice', 'id')
        # invlice map table
        self.im = table.get('InvoiceMap', 'id')
        # item-line table
        self.il = table.get('ItemLine', 'invoice_id')
        # customer table
        self.cs = table.get('Customer', 'id')
        # customer map table
        self.csm = table.get('CustomerMap', 'id')
        # product table
        self.p = table.get('Product', 'id')
        # product map table
        self.pm = table.get('ProductMap', 'id')
        # line-item table
        self.line_item = table.get('LineItem', 'invoice_id')
        # wc order
        api = wc_api.get()
        self.wco = wc.get(api, 'orders')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.i.set_connection(connection)
        self.im.set_connection(connection)
        self.il.set_connection(connection)
        self.cs.set_connection(connection)
        self.csm.set_connection(connection)
        self.p.set_connection(connection)
        self.pm.set_connection(connection)
        self.line_item.set_connection(connection)

    def _items(self, line_items):
        items = []
        for item in line_items:
            moeinid = self.pm.get('id', wcid=item['product_id']).id
            product = self.p.get('id', 'name', id=moeinid)
            items.append({
                'id': product.id,
                'name': product.name,
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': item['subtotal'],
                'total': item['total']
            })
        return items

    def _items_total(self, line_items):
        total = 0
        for item in line_items:
            total += int(item['subtotal'])
        return total

    def orders(self, status, after, before):
        orders = []
        ids = [row.wcid for row in self.im.all('wcid')]
        rows = self.wco.all(excludes=ids, status=status, after=after, before=before)
        for row in rows:
            row['created_date'] = datetime.fromisoformat(row['date_created_gmt'])
            row['items'] = self._items(row['line_items'])
            row['items_total'] = self._items_total(row['line_items'])
            orders.append(row)
        return orders

    def update_order(self, order_id, data):
        self.wco.update(order_id, data)

    def saved(self):
        saved = []
        rows = self.i.inner_join(
            self.im,
            'id',
            'id',
            [],
            ['wcid', 'last_update']
        )
        for row in rows:
            customer = self.cs.get('id', 'firstname', 'lastname', id=row.customer_id)
            saved.append({
                'id': row.id,
                'created_date': row.created_date,
                'customer_id': customer.id,
                'customer_firstname': customer.firstname,
                'customer_lastname': customer.lastname,
                'order_id': row.wcid,
                'saved_date': row.last_update
            })
        return saved

    def save(self, order):
        # detect customer
        wc_customer_id = order['customer_id']
        if wc_customer_id == 0:
            # customer is guest
            # get moein's guest customer id from settings
            customer_id = s.get('invoices')['guest']
        else:
            try:
                customer_id = self.csm.get('id', wcid=wc_customer_id).id
            except table.DoesNotExistsError:
                # customer does not exists, lets create
                fname = order['billing']['first_name'] or order['shipping']['first_name']
                lname = order['billing']['last_name'] or order['shipping']['last_name']
                self.cs.create({
                    'firstname': fname,
                    'lastname': lname
                })
                customer_id = self.cs.max_pk()
                self.csm.create({
                    'id': customer_id,
                    'wcid': wc_customer_id,
                    'last_update': datetime.now()
                })
        # create invoice
        self.i.create({
            'customer_id': customer_id,
            'created_date': order['created_date']
        })
        # get created invoice's id
        invoice_id = self.i.max_pk()
        for item in order['items']:
            self.line_item.create({
                'invoice_id': invoice_id,
                'product_id': item['id'],
                'quantity': item['quantity']
            })
        # map invoice to wc_order
        self.im.create({
            'id': invoice_id,
            'wcid': order['id'],
            'last_update': datetime.now()
        })

    def remove(self, order_id):
        # find invoice id
        invoice_id = self.im.get('id', wcid=order_id).id
        # remove related items to invoice
        self.line_item.delete(invoice_id=invoice_id)
        # remove invoice
        self.i.delete(id=invoice_id)
        # remove map
        self.im.delete(id=invoice_id)
