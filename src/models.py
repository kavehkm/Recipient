# standard
from datetime import datetime
# internal
from src import wc
from src import table
from src import wc_api
from src import settings as s


##############
# Exceptions #
##############
class DoesNotExists(Exception):
    """Does Not Exists Exception"""
    pass


##############
# Base Model #
##############
class Model(object):
    """Recipient Model"""
    def __init__(self):
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection

    def execute(self, sql, parameters=(), method=None):
        results = None
        cursor = self._connection.cursor()
        cursor.execute(sql, parameters)
        if method:
            results = getattr(cursor, method)()
        cursor.close()
        return results

    def max(self, table, column):
        sql = 'SELECT MAX({}) FROM {}'.format(column, table)
        return self.execute(sql, method='fetchval')


#############
# Map Model #
#############
class Map(Model):
    """Recipient Map"""
    def __init__(self, table, mappable_name):
        super().__init__()
        self.table = table
        self.mappable_name = mappable_name

    @staticmethod
    def where(conditions):
        params = list()
        sql = " WHERE "
        for column, value in conditions.items():
            sql += "{} = ? AND ".format(column)
            params.append(value)
        return sql.rstrip(" AND "), params

    def get(self, **conditions):
        sql = "SELECT * FROM {}".format(self.table)
        _sql, params = self.where(conditions)
        sql += _sql
        obj = self.execute(sql, params, method='fetchone')
        if obj is None:
            msg = 'Map for {} with '.format(self.mappable_name)
            for column, value in conditions.items():
                msg += '{} `{}`, '.format(column, value)
            msg = msg.rstrip(', ')
            msg += ' does not exists.'
            raise DoesNotExists(msg)
        return obj

    def all(self):
        sql = "SELECT * FROM {}".format(self.table)
        return self.execute(sql, method='fetchall')

    def filter(self, **conditions):
        sql = "SELECT * FROM {}".format(self.table)
        _sql, params = self.where(conditions)
        sql += _sql
        return self.execute(sql, params, method='fetchall')

    def create(self, mid, wcid, last_update=None):
        last_update = last_update or datetime.now()
        params = [mid, wcid, last_update]
        sql = "INSERT INTO {}(id, wcid, last_update) VALUES (?, ?, ?)".format(self.table)
        self.execute(sql, params)

    def update(self, fields, **conditions):
        params = list()
        sql = "UPDATE {} SET ".format(self.table)
        for column, value in fields.items():
            sql += "{} = ?, ".format(column)
            params.append(value)
        sql = sql.rstrip(', ')
        if conditions:
            _sql, _params = self.where(conditions)
            sql += _sql
            params.extend(_params)
        return self.execute(sql, params)

    def delete(self, **conditions):
        params = list()
        sql = "DELETE FROM {}".format(self.table)
        if conditions:
            _sql, params = self.where(conditions)
            sql += _sql
        return self.execute(sql, params)


##################
# Mappable Model #
##################
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


#################
# Product Model #
#################
class Product(Mappable):
    """Recipient Product Model"""
    def __init__(self):
        super().__init__()
        self.map = Map('ProductMap', 'product')
        self.wc = wc.get(wc_api.get(), 'products')

        self.repository =   1
        self.price_level =  1
        self.price_type =   2

    def set_connection(self, connection):
        super().set_connection(connection)
        self.map.set_connection(connection)

    def mapped(self):
        mapped = list()
        params = [self.repository, self.price_type, self.price_level]
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, PM.wcid, PM.last_update, PM.update_required, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            INNER JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            LEFT JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                KP.Type = ? AND KP.PriceID = ?
        """
        for row in self.execute(sql, params, method='fetchall'):
            mapped.append({
                'id': row.ID,
                'name': row.Name,
                'price': row.FinalPrice,
                'quantity': row.Mojoodi,
                'category_id': row.GroupID,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = list()
        params = [self.repository, self.price_type, self.price_level]
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            LEFT JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            LEFT JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                PM.id IS NULL AND KP.Type = ? AND KP.PriceID = ?
        """
        for row in self.execute(sql, params, method='fetchall'):
            unmapped.append({
                'id': row.ID,
                'name': row.Name,
                'price': row.FinalPrice,
                'quantity': row.Mojoodi,
                'category_id': row.GroupID,
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.map.all()
        ]

    def wc_unmapped(self):
        ids = [m.wcid for m in self.map.all()]
        return self.wc.all(excludes=ids)

    def add_map(self, moeinid, wcid, last_update):
        # check product
        sql = "SELECT Name FROM KalaList WHERE ID = ?"
        product = self.execute(sql, [moeinid], method='fetchone')
        if product is None:
            raise DoesNotExists('Product with id {} does not exists'.format(moeinid))
        # check woocommerce product
        self.wc.get(wcid)
        # everything is ok, lets create map
        self.map.create(moeinid, wcid, last_update)
        return {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update,
            'name': product.Name}

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check product
        sql = "SELECT Name FROM KalaList WHERE ID = ?"
        new_product = self.execute(sql, [new_moeinid], method='fetchone')
        if new_moeinid is None:
            raise DoesNotExists('Product with id {} does not exists'.format(new_moeinid))
        # check woocommerce product
        self.wc.get(new_wcid)
        # everything is ok, lets update current map
        self.map.update({'id': new_moeinid, 'wcid': new_wcid}, id=moeinid)
        return {
            'id': new_moeinid,
            'wcid': new_wcid,
            'name': new_product.Name
        }

    def remove_map(self, moeinid):
        # check for map
        self.map.get(id=moeinid)
        # map exists, lets delete it
        self.map.delete(id=moeinid)

    def wc_mapped_update(self, mapped):
        sql = """
            SELECT
                wcid
            FROM
                CategoryMap
            WHERE
                id = ?
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, [mapped['category_id']])
        category = cursor.fetchone()
        if category is None:
            # category map does not exists
            msg = 'Map for category {} does not exists.'.format(mapped['category_id'])
            raise DoesNotExists(msg)
        data = {
            'name': mapped['name'],
            'categories': [{'id': category.wcid}]
        }
        if mapped['quantity'] is not None:
            data['stock_quantity'] = mapped['quantity']
        self.wc.update(mapped['wcid'], data)
        # update product map
        sql = """
            UPDATE
                ProductMap
            SET
                last_update = ?
            WHERE
                id = ?
        """
        cursor.execute(sql, [datetime.now(), mapped['id']])
        cursor.close()

    def export2wc(self, product):
        sql = """
            SELECT
                wcid
            FROM
                CategoryMap
            WHERE
                id = ?
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, [product['category_id']])
        wc_category = cursor.fetchone()
        if wc_category is None:
            msg = 'Map for category {} does not exists.'.format(product['category_id'])
            raise DoesNotExists(msg)
        data = {
            'name': product['name'],
            'regular_price': str(product['price']),
            'categories': [{'id': wc_category.wcid}]
        }
        if product['quantity'] is not None:
            data['manage_stock'] = True
            data['stock_quantity'] = product['quantity']
        wc_product = self.wc.create(data)
        sql = """
            INSERT INTO
                ProductMap(id, wcid, last_update)
            VALUES
                (?, ?, ?)
        """
        cursor.execute(sql, [product['id'], wc_product['id']], datetime.now())
        cursor.close()

    def import2moein(self, wc_product):
        sql = """
            SELECT
                id
            FROM
                CategoryMap
            WHERE
                wcid = ?
        """
        wc_category = wc_product['categories'][0]
        cursor = self._connection.cursor()
        cursor.execute(sql, [wc_category['id']])
        category = cursor.fetchone()
        if category is None:
            msg = 'Map for category {} does not exists.'.format(wc_category['name'])
            raise DoesNotExists(msg)
        sql = """
            INSERT INTO
                KalaList(Name, GroupID)
            VALUES
                (?, ?)
        """
        cursor.execute(sql, [wc_product['name'], category.id])
        sql = """
            INSERT INTO
                ProductMap(id, wcid, last_update)
            VALUES
                (?, ?, ?)
        """
        cursor.execute(sql, [self.max('KalaList', 'ID'), wc_product['id'], datetime.now()])
        cursor.close()


##################
# Category Model #
##################
class Category(Mappable):
    """Recipient Category Model"""
    def __init__(self):
        super().__init__()
        self.map = Map('CategoryMap', 'category')
        self.wc = wc.get(wc_api.get(), 'products/categories')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.map.set_connection(connection)

    def hierarchy_name(self, category):
        # check for parent
        if not category['parent']:
            return category['name']
        sql = "SELECT ID, GroupKala, ParentID FROM GroupKala WHERE ID = ?"
        parent = self.execute(sql, [category['parent']], method='fetchone')
        if parent is None:
            return category['name']
        else:
            parent = {
                'id': parent.ID,
                'name': parent.GroupKala,
                'parent': parent.ParentID
            }
            return self.hierarchy_name(parent) + '___' + category['name']

    def wc_hierarchy_name(self, category, categories):
        # check for parent
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
        categories.sort(key=lambda c: c['parent'])

    def mapped(self):
        mapped = list()
        sql = """
            SELECT
                C.ID, C.ParentID, C.GroupKala, CM.id, CM.wcid, CM.last_update, CM.update_required
            FROM
                GroupKala as C
            INNER JOIN
                CategoryMap AS CM ON C.ID = CM.id
        """
        for row in self.execute(sql, method='fetchall'):
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
        unmapped = list()
        sql = """
            SELECT
                C.ID, C.ParentID, C.GroupKala
            FROM
                GroupKala as C
            LEFT JOIN
                CategoryMap as CM ON C.ID = CM.id
            WHERE
                CM.id IS NULL
        """
        for row in self.execute(sql, method='fetchall'):
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
            for row in self.map.all()
        ]

    def wc_unmapped(self):
        unmapped = list()
        ids = [m.wcid for m in self.map.all()]
        categories = self.wc.all()
        self.hierarchify(categories, woocommerce=True)
        for category in categories:
            if category['id'] not in ids:
                unmapped.append(category)
        return unmapped

    def add_map(self, moeinid, wcid, last_update):
        # check category and parent
        sql = "SELECT ID, GroupKala, ParentID FROM GroupKala WHERE ID = ?"
        category = self.execute(sql, [moeinid], method='fetchone')
        if category is None:
            raise DoesNotExists('Category with id {} does not exists.'.format(moeinid))
        if category.ParentID:
            self.map.get(id=category.ParentID)
        category = {
            'id': category.ID,
            'name': category.GroupKala,
            'parent': category.ParentID
        }
        # check woocommerce category
        self.wc.get(wcid)
        # everything is ok, lets create map
        self.map.create(moeinid, wcid, last_update)
        return {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update,
            'name': self.hierarchy_name(category)
        }

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check new category and parent
        sql = "SELECT ID, GroupKala, ParentID FROM GroupKala WHERE ID = ?"
        new_category = self.execute(sql, [new_moeinid], method='fetchone')
        if new_category is None:
            raise DoesNotExists('Category with id {} does not exists'.format(new_moeinid))
        if new_category.ParentID:
            self.map.get(id=new_category.ParentID)
        new_category = {
            'id': new_category.ID,
            'name': new_category.GroupKala,
            'parent': new_category.ParentID
        }
        # check for new woocommerce category
        self.wc.get(new_wcid)
        # everything is ok, lets update current map
        self.map.update({'id': new_moeinid, 'wcid': new_wcid}, id=moeinid)
        return {
            'id': new_moeinid,
            'wcid': new_wcid,
            'name': self.hierarchy_name(new_category)
        }

    def remove_map(self, moeinid):
        # check for map
        self.map.get(id=moeinid)
        # map exists, lets delete it
        self.map.delete(id=moeinid)

    def wc_mapped_update(self, mapped):
        data = {'name': mapped['_name']}
        # check for parent
        if mapped['parent']:
            parent = self.map.get(id=mapped['parent'])
            data['parent'] = parent.wcid
        # update woocommerce category
        self.wc.update(mapped['wcid'], data)
        # update category map
        self.map.update({'last_update': datetime.now()}, id=mapped['id'])

    def export2wc(self, category):
        data = {
            'name': category['_name'],
            'parent': category['parent']
        }
        # check for parent
        if category['parent']:
            parent = self.map.get(id=category['parent'])
            data['parent'] = parent.wcid
        # create woocommerce category
        wc_category = self.wc.create(data)
        self.map.create(category['id'], wc_category['id'])

    def import2moein(self, wc_category):
        # check for parent
        if wc_category['parent']:
            parent = self.map.get(wcid=wc_category['parent'])
            parent_id = parent.id
        else:
            parent_id = 0
        # create category
        sql = "INSERT INTO GroupKala(GroupKala, ParentID) VALUES (?, ?)"
        self.execute(sql, [wc_category['_name'], parent_id])
        # create map
        self.map.create(self.max('GroupKala', 'ID'), wc_category['id'])


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
