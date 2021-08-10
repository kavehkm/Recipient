# standard
from datetime import datetime
# internal
from src import wc
from src import table
from src import wc_api
from src import settings as s


class DoesNotExists(Exception):
    """Does Not Exists Exception"""
    pass


class Model(object):
    """Recipient Model"""
    def __init__(self):
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection

    def max(self, table_name, column):
        sql = "SELECT MAX({}) FROM {}".format(column, table_name)
        cursor = self._connection.cursor()
        cursor.execute(sql)
        m = cursor.fetchval()
        cursor.close()
        return m


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
        self.price_type =   2
        self.price_level =  1
        self.repository =   1
        # wc product
        self.wc = wc.get(wc_api.get(), 'products')

    def mapped(self):
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, PM.wcid, PM.last_update, PM.update_required, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            INNER JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            INNER JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                KP.Type = ? AND KP.PriceID = ?
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, [self.repository, self.price_type, self.price_level])
        rows = cursor.fetchall()
        cursor.close()
        mapped = list()
        for row in rows:
            mapped.append({
                'id':               row.ID,
                'name':             row.Name,
                'price':            row.FinalPrice,
                'quantity':         row.Mojoodi,
                'category_id':      row.GroupID,
                'wcid':             row.wcid,
                'last_update':      row.last_update,
                'update_required':  row.update_required
            })
        return mapped

    def unmapped(self):
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            LEFT JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            INNER JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                PM.id IS NULL AND KP.Type = ? AND KP.PriceID = ?
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, [self.repository, self.price_type, self.price_level])
        rows = cursor.fetchall()
        cursor.close()
        unmapped = list()
        for row in rows:
            unmapped.append({
                'id':           row.ID,
                'name':         row.Name,
                'price':        row.FinalPrice,
                'quantity':     row.Mojoodi,
                'category_id':  row.GroupID,
            })
        return unmapped

    def wc_mapped(self):
        sql = "SELECT wcid FROM ProductMap"
        cursor = self._connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return [{'id': row.wcid} for row in rows]

    def wc_unmapped(self):
        ids = [wcm['id'] for wcm in self.wc_mapped()]
        return self.wc.all(excludes=ids)

    def wc_mapped_update(self, mapped):
        sql = "SELECT wcid FROM CategoryMap WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [mapped['category_id']])
        category = cursor.fetchone()
        if category is None:
            # category map does not exists
            msg = 'Map for category {} does not exists.'.format(mapped['category_id'])
            raise DoesNotExists(msg)
        self.wc.update(mapped['wcid'], {
            'name': mapped['name'],
            'regular_price': str(mapped['price']),
            'stock_quantity': mapped['quantity'],
            'categories': [{'id': category.wcid}]
        })
        # update product map
        sql = "UPDATE ProductMap SET last_update = ? WHERE id = ?"
        cursor.execute(sql, [datetime.now(), mapped['id']])
        cursor.close()

    def add_map(self, moeinid, wcid, last_update):
        # check product
        sql = "SELECT Name FROM KalaList WHERE ID = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [moeinid])
        product = cursor.fetchone()
        if product is None:
            # product does not exists
            msg = 'Product with id {} does not exists.'.format(moeinid)
            raise DoesNotExists(msg)
        # check woocommerce product
        self.wc.get(wcid)
        # everything is ok, lets create map
        sql = "INSERT INTO ProductMap(id, wcid, last_update) VALUES (?, ?, ?)"
        cursor.execute(sql, [moeinid, wcid, last_update])
        cursor.close()
        return {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update,
            'name': product.Name}

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check product
        sql = "SELECT Name FROM KalaList WHERE ID = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [new_moeinid])
        new_product = cursor.fetchone()
        if new_product is None:
            # new product does not exists
            msg = 'Product with id {} does not exists.'.format(new_moeinid)
            raise DoesNotExists(msg)
        # check woocommerce product
        self.wc.get(new_wcid)
        # everything is ok lets update map
        sql = "UPDATE ProductMap SET id = ?, wcid = ? WHERE id = ?"
        cursor.execute(sql, [new_moeinid, new_wcid, moeinid])
        cursor.close()
        return {
            'id': new_moeinid,
            'wcid': new_wcid,
            'name': new_product.Name
        }

    def remove_map(self, moeinid):
        sql = "SELECT id FROM ProductMap WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [moeinid])
        product = cursor.fetchone()
        if product is None:
            # target product does not exists
            msg = 'Product with id {} does not exists.'.format(moeinid)
            raise DoesNotExists(msg)
        sql = "DELETE FROM ProductMap WHERE id = ?"
        cursor.execute(sql, [moeinid])
        cursor.close()

    def export2wc(self, product):
        sql = "SELECT wcid FROM CategoryMap WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [product['category_id']])
        wc_category = cursor.fetchone()
        if wc_category is None:
            msg = 'Map for category {} does not exists.'.format(product['category_id'])
            raise DoesNotExists(msg)
        wc_product = self.wc.create({
            'name': product['name'],
            'manage_stock': True,
            'regular_price': str(product['price']),
            'stock_quantity': product['quantity'],
            'categories': [{'id': wc_category.wcid}]
        })
        sql = "INSERT INTO ProductMap(id, wcid, last_update) VALUES (?, ?, ?)"
        cursor.execute(sql, [product['id'], wc_product['id']], datetime.now())
        cursor.close()

    def import2moein(self, wc_product):
        sql = "SELECT id FROM CategoryMap WHERE wcid = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [wc_product['categories'][0]])
        category = cursor.fetchone()
        if category is None:
            msg = 'Map for category {} does not exists.'.format(wc_product['categories'][0])
            raise DoesNotExists(msg)
        sql = "INSERT INTO KalaList(Name, GroupID) VALUES (?, ?)"
        cursor.execute(sql, [wc_product['name'], category.id])
        sql = "INSERT INTO ProductMap(id, wcid, last_update) VALUES (?, ?, ?)"
        cursor.execute(sql, [self.max('KalaList', 'ID'), wc_product['id'], datetime.now()])
        cursor.close()


class Category(Mappable):
    """Recipient Category Model"""
    def __init__(self):
        super().__init__()
        # category table
        self.c = table.get('GroupKala', 'ID')
        # category map table
        self.cm = table.get('CategoryMap', 'id')
        # wc category
        api = wc_api.get()
        self.wcc = wc.get(api, 'products/categories')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.c.set_connection(connection)
        self.cm.set_connection(connection)

    def hierarchy_name(self, category):
        if not category['parent']:
            return category['name']
        try:
            row = self.c.get('ID', 'GroupKala', 'ParentID', ID=category['parent'])
        except table.DoesNotExistsError:
            parent = None
        else:
            parent = {
                'id': row.ID,
                'name': row.GroupKala,
                'parent': row.ParentID
            }
        return self.hierarchy_name(parent) + '___' + category['name'] if parent else category['name']

    def wc_hierarchy_name(self, category, categories):
        if not category['parent']:
            return category['name']
        parent = None
        for cat in categories:
            if cat['id'] == category['parent']:
                parent = cat
                break
        return self.wc_hierarchy_name(parent, categories) + '___' + category['name'] if parent else category['name']

    def hierarchify(self, categories, woocommerce=False):
        for category in categories:
            category['_name'] = category['name']
            if woocommerce:
                category['name'] = self.wc_hierarchy_name(category, categories)
            else:
                category['name'] = self.hierarchy_name(category)
        categories.sort(key=lambda c: c['parent'] or 0)

    def mapped(self):
        mapped = []
        rows = self.c.inner_join(
            self.cm,
            'ID',
            'id',
            [],
            ['wcid', 'last_update', 'update_required']
        )
        for row in rows:
            mapped.append({
                'id': row.ID,
                'name': row.GroupKala,
                'parent': row.ParentID,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        self.hierarchify(mapped)
        return mapped

    def unmapped(self):
        unmapped = []
        rows = self.c.left_outer_join(
            self.cm,
            'ID',
            'id',
            []
        )
        for row in rows:
            unmapped.append({
                'id': row.ID,
                'name': row.GroupKala,
                'parent': row.ParentID
            })
        self.hierarchify(unmapped)
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.cm.all('wcid')
        ]

    def wc_unmapped(self):
        unmapped = []
        ids = [row.wcid for row in self.cm.all('wcid')]
        categories = self.wcc.all()
        self.hierarchify(categories, woocommerce=True)
        for category in categories:
            if category['id'] not in ids:
                unmapped.append(category)
        return unmapped

    def wc_mapped_update(self, mapped):
        data = {
            'name': mapped['_name']
        }
        if mapped['parent']:
            try:
                row = self.cm.get('wcid', id=mapped['parent'])
            except table.DoesNotExistsError:
                pass
            else:
                data['parent'] = row.wcid
        self.wcc.update(mapped['wcid'], data)
        self.cm.update({'last_update': datetime.now()}, id=mapped['id'])

    def add_map(self, moeinid, wcid, last_update):
        # check moeinid
        row = self.c.get('ID', 'GroupKala', 'ParentID', ID=moeinid)
        category = {
            'id': row.ID,
            'name': row.GroupKala,
            'parent': row.ParentID
        }
        # check wcid
        self.wcc.get(wcid)
        fields = {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        }
        self.cm.create(fields)
        fields['name'] = self.hierarchy_name(category)
        return fields

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check moeinid
        row = self.c.get('ID', 'GroupKala', 'ParentID', ID=new_moeinid)
        category = {
            'id': row.ID,
            'name': row.GroupKala,
            'parent': row.ParentID
        }
        # check wcid
        self.wcc.get(new_wcid)
        fields = {
            'id': new_moeinid,
            'wcid': new_wcid
        }
        self.cm.update(fields, id=moeinid)
        fields['name'] = self.hierarchy_name(category)
        return fields

    def remove_map(self, moeinid):
        self.cm.get(id=moeinid)
        self.cm.delete(id=moeinid)

    def export2wc(self, category):
        if category['parent']:
            row = self.cm.get('wcid', id=category['parent'])
            parent_id = row.wcid
        else:
            parent_id = 0
        wc_category = self.wcc.create({
            'name': category['_name'],
            'parent': parent_id
        })
        self.cm.create({
            'id': category['id'],
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_category):
        if wc_category['parent']:
            row = self.cm.get('id', wcid=wc_category['parent'])
            parent_id = row.id
        else:
            parent_id = None
        self.c.create({
            'GroupKala': wc_category['_name'],
            'ParentID': parent_id
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
